import settings

test_example = """from pathlib import Path

DATABASES = {
}

INSTALLED_APPS = [
    \"previously_installed\",
]"""


def test_add_installed_apps_keeps_previous():
    actual = settings.add_installed_apps(test_example, "users")
    assert '"previously_installed",' in actual


def test_add_installed_apps_adds_rest_framework():
    actual = settings.add_installed_apps(test_example, "users")
    assert '"rest_framework",' in actual


def test_add_installed_apps_adds_users():
    actual = settings.add_installed_apps(test_example, "users")
    assert '"users",' in actual


def test_change_database_settings():
    actual = settings.change_database_settings(test_example)
    expected = """DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}"""
    assert expected in actual


def test_add_new_settings_users():
    actual = settings.add_new_settings(test_example, "users")
    assert 'AUTH_USER_MODEL = "users.UserAccount"' in actual


def test_add_new_settings_siteid():
    actual = settings.add_new_settings(test_example, "users")
    assert "SITE_ID = 1" in actual
