import pytest
import settings

test_example = """from pathlib import Path

SECRET_KEY = "secret"
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    }
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

INSTALLED_APPS = [
    \"previously_installed\",
]"""


class TestAddInstalledApps:
    def test_keeps_previous(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"previously_installed",' in actual

    def test_adds_sites(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"django.contrib.sites",' in actual

    def test_adds_rest_framework(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"rest_framework",' in actual

    def test_adds_rest_framework_authtoken(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"rest_framework.authtoken",' in actual

    def test_adds_allauth(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"allauth",' in actual

    def test_adds_allauth_account(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"allauth.account",' in actual

    def test_adds_dj_rest_auth(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"dj_rest_auth",' in actual

    def test_adds_dj_rest_auth_registration(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"dj_rest_auth.registration",' in actual

    def test_adds_users(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"users",' in actual


class TestChangeDatabaseSettings:
    @pytest.fixture
    def setup(self):
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
        return actual, expected

    def test_content(self, setup):
        actual, expected = setup
        assert expected in actual

    def test_does_not_eat_next_section(self, setup):
        actual, _ = setup
        assert "TEMPLATES = [" in actual

    def test_not_double_closed(self, setup):
        actual, expected = setup
        expected = expected + "\n}"
        assert expected not in actual


def test_set_project_template_dir():
    actual = settings.set_project_template_dir(test_example)
    assert '"DIRS": [BASE_DIR / "templates"],' in actual


class TestAddNewSettings:
    def test_user_model(self):
        actual = settings.add_new_settings(test_example, "users")
        assert 'AUTH_USER_MODEL = "users.UserAccount"' in actual

    def testsiteid(self):
        actual = settings.add_new_settings(test_example, "users")
        assert "SITE_ID = 1" in actual

    def test_login_redirect(self):
        actual = settings.add_new_settings(test_example, "users")
        assert 'LOGIN_REDIRECT_URL = "home"' in actual

    def test_logout_redirect(self):
        actual = settings.add_new_settings(test_example, "users")
        assert 'LOGOUT_REDIRECT_URL = "home"' in actual

    def test_no_login_redirect(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        assert "LOGIN_REDIRECT_URL" not in actual

    def test_no_logout_redirect(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        assert "LOGOUT_REDIRECT_URL" not in actual


def test_add_import_os():
    actual = actual = settings.add_import_os(test_example)
    assert "import os" in actual


def test_set_secret_key():
    actual = settings.set_secret_key(test_example)
    assert 'SECRET_KEY = os.environ.get("SECRET_KEY")' in actual


def test_set_debug():
    actual = settings.set_debug(test_example)
    assert 'DEBUG = int(os.environ.get("DEBUG", default=1))' in actual


def test_set_allowed_hosts():
    actual = settings.set_allowed_hosts(test_example)
    expected = 'ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")'
    assert expected in actual


def test_add_prod_rest_framework():
    actual = settings.add_prod_rest_framework_renderer(test_example)
    expected = """if not DEBUG:
    REST_FRAMEWORK[
        "DEFAULT_RENDERER_CLASSES"
    ] = "rest_framework.renderers.JSONRenderer"
"""
    assert expected in actual


def test_remove_password_validators():
    actual = settings.remove_password_validators(test_example)
    print(actual)
    assert "AUTH_PASSWORD_VALIDATORS = []" in actual
    assert "TEMPLATES = [" in actual
