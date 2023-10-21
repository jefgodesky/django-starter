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
