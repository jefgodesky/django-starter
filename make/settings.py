import os
import re

import black


def add_installed_apps(settings: str, users: str, providers=None):
    apps_to_mix = ['"django.contrib.sites"']
    apps_to_add = [
        '"django.contrib.sites"',
        '"rest_framework"',
        '"rest_framework.authtoken"',
        '"allauth"',
        '"allauth.account"',
    ]

    if providers:
        apps_to_add.append('"allauth.socialaccount"')
        for provider in providers:
            apps_to_add.append(f'"allauth.socialaccount.providers.{provider}"')

    apps_to_add = apps_to_add + [
        '"dj_rest_auth"',
        '"dj_rest_auth.registration"',
        '"drf_yasg"',
        f'"{users}"',
    ]

    match = re.search(r"INSTALLED_APPS = \[(.*?)]", settings, flags=re.DOTALL)
    if not match:
        return settings
    apps_existing_str = match.group(1).strip()
    apps_existing = [app.strip() for app in apps_existing_str.split(",") if app]
    apps = sorted(apps_existing + apps_to_mix) + apps_to_add
    apps_str = ",\n    ".join(apps)
    installed_str = f"INSTALLED_APPS = [\n    {apps_str},\n]"
    return settings.replace(match.group(0), installed_str)


def change_database_settings(settings: str):
    pattern = r"DATABASES = {(\s*)['|\"]default['|\"]: {([\S\s]*?)\n\}"
    match_databases = re.search(pattern, settings, flags=re.DOTALL)
    if not match_databases:
        return settings
    databases = """if TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get(
                "SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")
            ),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }
"""

    return settings.replace(match_databases.group(0), f"DATABASES = {databases}")


def set_project_template_dir(settings: str):
    templates_pattern = r"TEMPLATES = \[(\s*){[\s\S]*},?(\s)*]"
    match_templates = re.search(templates_pattern, settings, flags=re.DOTALL)
    if not match_templates:
        return settings
    dirs_pattern = r"['|\"]DIRS['|\"]: \[\]"
    match_dirs = re.search(dirs_pattern, match_templates.group(0), flags=re.DOTALL)
    if not match_dirs:
        return settings
    dirs_update = '"DIRS": [BASE_DIR / "templates"]'
    updated_templates = match_templates.group(0).replace("'DIRS': []", dirs_update)
    updated_templates = updated_templates.replace('"DIRS": []', dirs_update)
    return settings.replace(match_templates.group(0), updated_templates)


def add_new_settings(settings: str, users: str, api_only: bool = False):
    new_settings_anchor = "from pathlib import Path"
    api_base = "v1/" if api_only else "api/v1/"
    new_settings = [
        f'AUTH_USER_MODEL = "{users}.UserAccount"',
        "SITE_ID = 1",
        f'API_BASE = "{api_base}"',
        "USER_DETAILS_PUBLIC = False",
        'ACCOUNT_EMAIL_VERIFICATION = "mandatory"',
        "ACCOUNT_EMAIL_REQUIRED = True",
        'ACCOUNT_AUTHENTICATION_METHOD = "username_email"',
        'EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"',
    ]
    if not api_only:
        new_settings.append('LOGIN_REDIRECT_URL = "home"')
        new_settings.append('LOGOUT_REDIRECT_URL = "home"')
    new_settings_string = (
        new_settings_anchor
        + os.linesep
        + os.linesep
        + os.linesep.join(new_settings)
        + os.linesep
    )
    return settings.replace(new_settings_anchor, new_settings_string)


def add_import_os(settings: str):
    anchor = "from pathlib import Path"
    replacement = "import os" + os.linesep + anchor
    return settings.replace(anchor, replacement)


def set_secret_key(settings: str):
    find = r'SECRET_KEY = "(.*)"'
    replacement = 'SECRET_KEY = os.environ.get("SECRET_KEY")'
    return re.sub(find, replacement, settings)


def set_debug(settings: str):
    find = r"DEBUG = (.*)\n"
    lines = [
        'DEBUG = int(os.environ.get("DEBUG", default=1))',
        'TESTING = os.environ.get("DJANGO_TESTING") == "1"',
    ]
    replacement = os.linesep.join(lines)
    return re.sub(find, replacement, settings)


def set_allowed_hosts(settings: str):
    find = r"ALLOWED_HOSTS = \[\]"
    replacement = 'ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")'
    return re.sub(find, replacement, settings)


def add_prod_rest_framework_renderer(settings: str):
    addendum = """if not DEBUG:
    REST_FRAMEWORK[
        "DEFAULT_RENDERER_CLASSES"
    ] = "rest_framework.renderers.JSONRenderer"
"""
    return settings + os.linesep + os.linesep + addendum


def add_authentication_backends(settings: str):
    addendum = """AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
"""
    return settings + os.linesep + os.linesep + addendum


def remove_password_validators(settings: str):
    pattern = r"AUTH_PASSWORD_VALIDATORS = \[[\s\S]*?]"
    return re.sub(pattern, "AUTH_PASSWORD_VALIDATORS = []", settings)


def add_social_auth_providers(settings: str, providers: dict):
    addendum = "SOCIALACCOUNT_PROVIDERS = {" + os.linesep
    for provider in providers:
        prefix = "SNAPCHAT" if provider == "snap" else provider.upper()
        patreon_scope = [
            '"identity"',
            '"identity[email]"',
            '"campaigns"',
            '"campaigns.members"',
        ]
        scopes = {
            "facebook": '"email", "public_profile"',
            "github": '"user"',
            "google": '"profile", "email"',
            "linkedin": '"r_basicprofile", "r_emailaddress"',
            "patreon": " ".join(patreon_scope),
            "reddit": '"identity"',
        }

        scope = scopes[provider] if provider in scopes.keys() else '"read"'
        addendum += f'"{provider}": {{'

        if provider == "auth0":
            addendum += f'"AUTH0_URL": os.environ.get("{prefix}_URL"),'
            addendum += '"OAUTH_PKCE_ENABLED": True,'

        if provider == "facebook":
            addendum += '"METHOD": "oauth2",'
            addendum += '"INIT_PARAMS": {"cookie": True},'
            addendum += '"FIELDS": ["id", "first_name", "last_name", "middle_name", \
                        "name", "name_format", "picture", "short_name"],'

        if provider == "google":
            addendum += '"AUTH_PARAMS": {"access_type": "online"},'
            addendum += '"OAUTH_PKCE_ENABLED": True,'

        if provider == "linkedin":
            addendum += (
                '"PROFILE_FIELDS": ["id", "first-name", "last-name",'
                '"email-address", "picture-url", "public-profile-url"],'
            )

        if provider == "patreon":
            addendum += '"VERSION": "v2",'

        if provider == "reddit":
            addendum += '"AUTH_PARAMS": {"duration": "permanent"},'
            addendum += (
                '"USER_AGENT": "django:myappid:1.0 (by /u/" /'
                '+ os.environ.get("REDDIT_USERNAME") + ")",'
            )

        addendum += '"APP": {'
        addendum += f'"client_id": os.environ.get("{prefix}_CLIENT_ID"),'
        addendum += f'"secret": os.environ.get("{prefix}_SECRET"),'
        addendum += f'"key": os.environ.get("{prefix}_KEY"),'

        if provider == "apple":
            addendum += '"settings": {'
            addendum += f'"certificate_key": os.environ.get("{prefix}_CERTIFICATE_KEY")'
            addendum += "},"

        addendum += "},"
        addendum += f'"SCOPE": [{scope}]'
        addendum += "},"
    addendum += "}"

    return black.format_str(
        settings + os.linesep + os.linesep + addendum, mode=black.FileMode()
    )
