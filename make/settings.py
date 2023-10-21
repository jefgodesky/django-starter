import os
import re


def add_installed_apps(settings: str, users: str):
    apps_to_add = ['"rest_framework"', f'"{users}"']
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
    match_databases = re.search(r"DATABASES = {[^}]*}", settings, flags=re.DOTALL)
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


def add_new_settings(settings: str, users: str):
    new_settings_anchor = "from pathlib import Path"
    new_settings = [f'AUTH_USER_MODEL = "{users}.UserAccount"', "SITE_ID = 1"]
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
