import os
import re


def add_installed_apps(settings: str, users: str):
    apps_to_add = [
        '"django.contrib.sites"',
        '"rest_framework"',
        '"rest_framework.authtoken"',
        '"allauth"',
        '"allauth.account"',
        '"dj_rest_auth"',
        '"dj_rest_auth.registration"',
        f'"{users}"',
    ]
    match = re.search(r"INSTALLED_APPS = \[(.*?)]", settings, flags=re.DOTALL)
    if not match:
        return settings
    apps_existing_str = match.group(1).strip()
    apps_existing = [app.strip() for app in apps_existing_str.split(",") if app]
    apps = apps_existing + apps_to_add
    apps_str = ",\n    ".join(apps)
    installed_str = f"INSTALLED_APPS = [\n    {apps_str},\n]"
    return settings.replace(match.group(0), installed_str)


def change_database_settings(settings: str):
    pattern = r"DATABASES = {(\s*)['|\"]default['|\"]: {([\S\s]*?)\n\}"
    match_databases = re.search(pattern, settings, flags=re.DOTALL)
    if not match_databases:
        return settings
    databases = """{
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}"""
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
    new_settings = [f'AUTH_USER_MODEL = "{users}.UserAccount"', "SITE_ID = 1"]
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
    replacement = 'DEBUG = int(os.environ.get("DEBUG", default=1))'
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


def remove_password_validators(settings: str):
    pattern = r"AUTH_PASSWORD_VALIDATORS = \[[\s\S]*?]"
    return re.sub(pattern, "AUTH_PASSWORD_VALIDATORS = []", settings)


def get_social_auth_providers(providers):
    config = {}
    for provider in providers:
        prefix = provider.upper()
        config[provider] = {
            "APP": {
                "client_id": f'os.environ.get("{prefix}_CLIENT_ID")',
                "secret": f'os.environ.get("{prefix}_SECRET")',
                "key": f'os.environ.get("{prefix}_KEY")',
            },
            "SCOPE": ["read", "write"],
        }

        if provider == "apple":
            config[provider]["APP"]["settings"] = {
                "certificate_key": f'os.environ.get("{prefix}_CERTIFICATE_KEY")'
            }

        if provider == "auth0":
            config[provider]["AUTH0_URL"] = f'os.environ.get("{prefix}_URL")'
            config[provider]["OAUTH_PKCE_ENABLED"] = True

        if provider == "digitalocean":
            config[provider]["SCOPE"] = ["read write"]

        if provider == "facebook":
            fields = [
                "id",
                "first_name",
                "last_name",
                "middle_name",
                "name",
                "name_format",
                "picture",
                "short_name",
            ]
            config[provider]["METHOD"] = "oauth2"
            config[provider]["INIT_PARAMS"] = {"cookie": True}
            config[provider]["FIELDS"] = fields
            config[provider]["SCOPE"] = ["email", "public_profile"]

        if provider == "github":
            config[provider]["SCOPE"] = ["user"]

        if provider == "google":
            config[provider]["AUTH_PARAMS"] = {"access_type": "online"}
            config[provider]["OAUTH_PKCE_ENABLED"] = True
            config[provider]["SCOPE"] = ["profile", "email"]

        if provider == "linkedin":
            fields = [
                "id",
                "first-name",
                "last-name",
                "email-address",
                "picture-url",
                "public-profile-url",
            ]
            config[provider]["PROFILE_FIELDS"] = fields
            config[provider]["SCOPE"] = ["r_basicprofile", "r_emailaddress"]

        if provider == "patreon":
            scope = ["identity", "identity[email]", "campaigns", "campaigns.members"]
            config[provider]["VERSION"] = "v2"
            config[provider]["SCOPE"] = scope

    return config
