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

    def test_add_allauth_socialaccount(self):
        actual = settings.add_installed_apps(test_example, "users", providers=["apple"])
        assert '"allauth.socialaccount",' in actual

    def test_add_allauth_socialaccount_auth0(self):
        actual = settings.add_installed_apps(test_example, "users", providers=["auth0"])
        assert '"allauth.socialaccount.providers.auth0",' in actual

    def test_add_allauth_socialaccount_digitalocean(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["digitalocean"]
        )
        assert '"allauth.socialaccount.providers.digitalocean",' in actual

    def test_add_allauth_socialaccount_discord(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["discord"]
        )
        assert '"allauth.socialaccount.providers.discord",' in actual

    def test_add_allauth_socialaccount_facebook(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["facebook"]
        )
        assert '"allauth.socialaccount.providers.facebook",' in actual

    def test_add_allauth_socialaccount_github(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["github"]
        )
        assert '"allauth.socialaccount.providers.github",' in actual

    def test_add_allauth_socialaccount_google(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["google"]
        )
        assert '"allauth.socialaccount.providers.google",' in actual

    def test_add_allauth_socialaccount_instagram(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["instagram"]
        )
        assert '"allauth.socialaccount.providers.instagram",' in actual

    def test_add_allauth_socialaccount_linkedin(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["linkedin"]
        )
        assert '"allauth.socialaccount.providers.linkedin",' in actual

    def test_add_allauth_socialaccount_patreon(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["patreon"]
        )
        assert '"allauth.socialaccount.providers.patreon",' in actual

    def test_add_allauth_socialaccount_reddit(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["reddit"]
        )
        assert '"allauth.socialaccount.providers.reddit",' in actual

    def test_add_allauth_socialaccount_slack(self):
        actual = settings.add_installed_apps(test_example, "users", providers=["slack"])
        assert '"allauth.socialaccount.providers.slack",' in actual

    def test_add_allauth_socialaccount_snap(self):
        actual = settings.add_installed_apps(test_example, "users", providers=["snap"])
        assert '"allauth.socialaccount.providers.snap",' in actual

    def test_add_allauth_socialaccount_twitch(self):
        actual = settings.add_installed_apps(
            test_example, "users", providers=["twitch"]
        )
        assert '"allauth.socialaccount.providers.twitch",' in actual

    def test_add_allauth_socialaccount_apple(self):
        actual = settings.add_installed_apps(test_example, "users", providers=["apple"])
        assert '"allauth.socialaccount.providers.apple",' in actual

    def test_adds_dj_rest_auth(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"dj_rest_auth",' in actual

    def test_adds_dj_rest_auth_registration(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"dj_rest_auth.registration",' in actual

    def test_drf_yasg(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"drf_yasg",' in actual

    def test_adds_users(self):
        actual = settings.add_installed_apps(test_example, "users")
        assert '"users",' in actual


class TestChangeDatabaseSettings:
    @pytest.fixture
    def setup(self):
        actual = settings.change_database_settings(test_example)
        expected = """
if TESTING:
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

    def test_siteid(self):
        actual = settings.add_new_settings(test_example, "users")
        assert "SITE_ID = 1" in actual

    def test_api_base(self):
        actual = settings.add_new_settings(test_example, "users")
        assert 'API_BASE = "api/v1/"' in actual

    def test_api_only_base(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        assert 'API_BASE = "v1/"' in actual

    def test_user_details_public(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        assert "USER_DETAILS_PUBLIC = False" in actual

    def test_email_verification(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        assert 'ACCOUNT_EMAIL_VERIFICATION = "mandatory"' in actual

    def test_email_required(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        assert "ACCOUNT_EMAIL_REQUIRED = True" in actual

    def test_authentication_method(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        assert 'ACCOUNT_AUTHENTICATION_METHOD = "username_email"' in actual

    def test_email_backend(self):
        actual = settings.add_new_settings(test_example, "users", api_only=True)
        backend = "django.core.mail.backends.console.EmailBackend"
        assert f'EMAIL_BACKEND = "{backend}"' in actual

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


class TestSetDebug:
    def test_set_debug(self):
        actual = settings.set_debug(test_example)
        assert 'DEBUG = int(os.environ.get("DEBUG", default=1))' in actual

    def test_set_testing(self):
        actual = settings.set_debug(test_example)
        assert 'TESTING = os.environ.get("DJANGO_TESTING") == "1"' in actual


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


def test_add_authentication_backends():
    actual = settings.add_authentication_backends(test_example)
    expected = """
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
"""
    assert expected in actual


def test_remove_password_validators():
    actual = settings.remove_password_validators(test_example)
    print(actual)
    assert "AUTH_PASSWORD_VALIDATORS = []" in actual
    assert "TEMPLATES = [" in actual


class TestAddSocialAuthProviders:
    def test_apple(self):
        actual = settings.add_social_auth_providers(test_example, ["apple"])
        assert '"apple": {' in actual
        assert '"client_id": os.environ.get("APPLE_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("APPLE_SECRET"),' in actual
        assert '"key": os.environ.get("APPLE_KEY"),' in actual
        assert '"certificate_key": os.environ.get("APPLE_CERTIFICATE_KEY")' in actual
        assert '"SCOPE": ["read"],' in actual

    def test_auth0(self):
        actual = settings.add_social_auth_providers(test_example, ["auth0"])
        assert '"auth0": {' in actual
        assert '"client_id": os.environ.get("AUTH0_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("AUTH0_SECRET"),' in actual
        assert '"key": os.environ.get("AUTH0_KEY"),' in actual
        assert '"AUTH0_URL": os.environ.get("AUTH0_URL"),' in actual
        assert '"OAUTH_PKCE_ENABLED": True,' in actual
        assert '"SCOPE": ["read"],' in actual

    def test_digitalocean(self):
        actual = settings.add_social_auth_providers(test_example, ["digitalocean"])
        assert '"digitalocean": {' in actual
        assert '"client_id": os.environ.get("DIGITALOCEAN_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("DIGITALOCEAN_SECRET"),' in actual
        assert '"key": os.environ.get("DIGITALOCEAN_KEY"),' in actual
        assert '"SCOPE": ["read"],' in actual

    def test_discord(self):
        actual = settings.add_social_auth_providers(test_example, ["discord"])
        assert '"discord": {' in actual
        assert '"client_id": os.environ.get("DISCORD_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("DISCORD_SECRET"),' in actual
        assert '"key": os.environ.get("DISCORD_KEY"),' in actual
        assert '"SCOPE": ["read"],' in actual

    def test_facebook(self):
        actual = settings.add_social_auth_providers(test_example, ["facebook"])
        assert '"facebook": {' in actual
        assert '"client_id": os.environ.get("FACEBOOK_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("FACEBOOK_SECRET"),' in actual
        assert '"key": os.environ.get("FACEBOOK_KEY"),' in actual
        assert '"METHOD": "oauth2",' in actual
        assert '"INIT_PARAMS": {"cookie": True},' in actual
        assert '"FIELDS": [' in actual
        assert '"id",' in actual
        assert '"first_name",' in actual
        assert '"last_name",' in actual
        assert '"middle_name",' in actual
        assert '"name",' in actual
        assert '"name_format",' in actual
        assert '"picture",' in actual
        assert '"short_name",' in actual
        assert '"SCOPE": ["email", "public_profile"],' in actual

    def test_github(self):
        actual = settings.add_social_auth_providers(test_example, ["github"])
        assert '"github": {' in actual
        assert '"client_id": os.environ.get("GITHUB_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("GITHUB_SECRET"),' in actual
        assert '"key": os.environ.get("GITHUB_KEY"),' in actual
        assert '"SCOPE": ["user"],' in actual

    def test_google(self):
        actual = settings.add_social_auth_providers(test_example, ["google"])
        assert '"google": {' in actual
        assert '"client_id": os.environ.get("GOOGLE_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("GOOGLE_SECRET"),' in actual
        assert '"key": os.environ.get("GOOGLE_KEY"),' in actual
        assert '"AUTH_PARAMS": {"access_type": "online"},' in actual
        assert '"OAUTH_PKCE_ENABLED": True,' in actual
        assert '"SCOPE": ["profile", "email"],' in actual

    def test_instagram(self):
        actual = settings.add_social_auth_providers(test_example, ["instagram"])
        assert '"instagram": {' in actual
        assert '"client_id": os.environ.get("INSTAGRAM_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("INSTAGRAM_SECRET"),' in actual
        assert '"key": os.environ.get("INSTAGRAM_KEY"),' in actual
        assert '"SCOPE": ["read"],' in actual

    def test_linkedin(self):
        actual = settings.add_social_auth_providers(test_example, ["linkedin"])
        assert '"linkedin": {' in actual
        assert '"client_id": os.environ.get("LINKEDIN_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("LINKEDIN_SECRET"),' in actual
        assert '"key": os.environ.get("LINKEDIN_KEY"),' in actual
        assert '"PROFILE_FIELDS": [' in actual
        assert '"id",' in actual
        assert '"first-name",' in actual
        assert '"last-name",' in actual
        assert '"email-address",' in actual
        assert '"picture-url",' in actual
        assert '"public-profile-url",' in actual
        assert '"SCOPE": ["r_basicprofile", "r_emailaddress"],' in actual

    def test_patreon(self):
        actual = settings.add_social_auth_providers(test_example, ["patreon"])
        assert '"patreon": {' in actual
        assert '"client_id": os.environ.get("PATREON_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("PATREON_SECRET"),' in actual
        assert '"key": os.environ.get("PATREON_KEY"),' in actual
        assert '"VERSION": "v2",' in actual
        assert '"SCOPE": [' in actual
        assert '"identity"' in actual
        assert '"identity[email]"' in actual
        assert '"campaigns"' in actual
        assert '"campaigns.members"' in actual

    def test_reddit(self):
        actual = settings.add_social_auth_providers(test_example, ["reddit"])
        assert '"reddit": {' in actual
        assert '"client_id": os.environ.get("REDDIT_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("REDDIT_SECRET"),' in actual
        assert '"key": os.environ.get("REDDIT_KEY"),' in actual
        assert '"SCOPE": ["identity"],' in actual
        assert '"AUTH_PARAMS": {"duration": "permanent"},' in actual
        assert '"USER_AGENT": "django:myappid:1.0 (by /u/"' in actual

    def test_slack(self):
        actual = settings.add_social_auth_providers(test_example, ["slack"])
        assert '"slack": {' in actual
        assert '"client_id": os.environ.get("SLACK_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("SLACK_SECRET"),' in actual
        assert '"key": os.environ.get("SLACK_KEY"),' in actual
        assert '"SCOPE": ["read"],' in actual

    def test_snapchat(self):
        actual = settings.add_social_auth_providers(test_example, ["snap"])
        assert '"snap": {' in actual
        assert '"client_id": os.environ.get("SNAPCHAT_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("SNAPCHAT_SECRET"),' in actual
        assert '"key": os.environ.get("SNAPCHAT_KEY"),' in actual
        assert '"SCOPE": ["read"],' in actual

    def test_twitch(self):
        actual = settings.add_social_auth_providers(test_example, ["twitch"])
        assert '"twitch": {' in actual
        assert '"client_id": os.environ.get("TWITCH_CLIENT_ID"),' in actual
        assert '"secret": os.environ.get("TWITCH_SECRET"),' in actual
        assert '"key": os.environ.get("TWITCH_KEY"),' in actual
        assert '"SCOPE": ["read"],' in actual
