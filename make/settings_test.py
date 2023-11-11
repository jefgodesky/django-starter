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


class TestSocialAccountProviders:
    def test_apple(self):
        providers = settings.get_social_auth_providers(["apple"])
        app = providers["apple"]["APP"]
        certkey = app["settings"]["certificate_key"]
        assert app["client_id"] == 'os.environ.get("APPLE_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("APPLE_SECRET")'
        assert app["key"] == 'os.environ.get("APPLE_KEY")'
        assert certkey == 'os.environ.get("APPLE_CERTIFICATE_KEY")'
        assert providers["apple"]["SCOPE"] == ["read"]

    def test_auth0(self):
        providers = settings.get_social_auth_providers(["auth0"])
        app = providers["auth0"]["APP"]
        assert app["client_id"] == 'os.environ.get("AUTH0_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("AUTH0_SECRET")'
        assert app["key"] == 'os.environ.get("AUTH0_KEY")'
        assert providers["auth0"]["AUTH0_URL"] == 'os.environ.get("AUTH0_URL")'
        assert providers["auth0"]["OAUTH_PKCE_ENABLED"] is True
        assert providers["auth0"]["SCOPE"] == ["read"]

    def test_digitalocean(self):
        providers = settings.get_social_auth_providers(["digitalocean"])
        app = providers["digitalocean"]["APP"]
        assert app["client_id"] == 'os.environ.get("DIGITALOCEAN_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("DIGITALOCEAN_SECRET")'
        assert app["key"] == 'os.environ.get("DIGITALOCEAN_KEY")'
        assert providers["digitalocean"]["SCOPE"] == ["read"]

    def test_discord(self):
        providers = settings.get_social_auth_providers(["discord"])
        app = providers["discord"]["APP"]
        assert app["client_id"] == 'os.environ.get("DISCORD_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("DISCORD_SECRET")'
        assert app["key"] == 'os.environ.get("DISCORD_KEY")'
        assert providers["discord"]["SCOPE"] == ["read"]

    def test_facebook(self):
        providers = settings.get_social_auth_providers(["facebook"])
        fb = providers["facebook"]
        app = fb["APP"]
        assert fb["METHOD"] == "oauth2"
        assert fb["INIT_PARAMS"]["cookie"] is True
        assert "id" in fb["FIELDS"]
        assert "first_name" in fb["FIELDS"]
        assert "last_name" in fb["FIELDS"]
        assert "middle_name" in fb["FIELDS"]
        assert "name" in fb["FIELDS"]
        assert "name_format" in fb["FIELDS"]
        assert "picture" in fb["FIELDS"]
        assert "short_name" in fb["FIELDS"]
        assert app["client_id"] == 'os.environ.get("FACEBOOK_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("FACEBOOK_SECRET")'
        assert app["key"] == 'os.environ.get("FACEBOOK_KEY")'
        assert providers["facebook"]["SCOPE"] == ["email", "public_profile"]

    def test_github(self):
        providers = settings.get_social_auth_providers(["github"])
        app = providers["github"]["APP"]
        assert app["client_id"] == 'os.environ.get("GITHUB_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("GITHUB_SECRET")'
        assert app["key"] == 'os.environ.get("GITHUB_KEY")'
        assert providers["github"]["SCOPE"] == ["user"]

    def test_google(self):
        providers = settings.get_social_auth_providers(["google"])
        app = providers["google"]["APP"]
        assert providers["google"]["AUTH_PARAMS"]["access_type"] == "online"
        assert providers["google"]["OAUTH_PKCE_ENABLED"] is True
        assert app["client_id"] == 'os.environ.get("GOOGLE_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("GOOGLE_SECRET")'
        assert app["key"] == 'os.environ.get("GOOGLE_KEY")'
        assert providers["google"]["SCOPE"] == ["profile", "email"]

    def test_instagram(self):
        providers = settings.get_social_auth_providers(["instagram"])
        app = providers["instagram"]["APP"]
        assert app["client_id"] == 'os.environ.get("INSTAGRAM_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("INSTAGRAM_SECRET")'
        assert app["key"] == 'os.environ.get("INSTAGRAM_KEY")'
        assert providers["instagram"]["SCOPE"] == ["read"]

    def test_linkedin(self):
        providers = settings.get_social_auth_providers(["linkedin"])
        app = providers["linkedin"]["APP"]
        assert "id" in providers["linkedin"]["PROFILE_FIELDS"]
        assert "first-name" in providers["linkedin"]["PROFILE_FIELDS"]
        assert "last-name" in providers["linkedin"]["PROFILE_FIELDS"]
        assert "email-address" in providers["linkedin"]["PROFILE_FIELDS"]
        assert "picture-url" in providers["linkedin"]["PROFILE_FIELDS"]
        assert "public-profile-url" in providers["linkedin"]["PROFILE_FIELDS"]
        assert app["client_id"] == 'os.environ.get("LINKEDIN_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("LINKEDIN_SECRET")'
        assert app["key"] == 'os.environ.get("LINKEDIN_KEY")'
        assert providers["linkedin"]["SCOPE"] == ["r_basicprofile", "r_emailaddress"]

    def test_patreon(self):
        providers = settings.get_social_auth_providers(["patreon"])
        app = providers["patreon"]["APP"]
        assert providers["patreon"]["VERSION"] == "v2"
        assert app["client_id"] == 'os.environ.get("PATREON_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("PATREON_SECRET")'
        assert app["key"] == 'os.environ.get("PATREON_KEY")'
        assert providers["patreon"]["SCOPE"] == [
            "identity",
            "identity[email]",
            "campaigns",
            "campaigns.members",
        ]

    def test_reddit(self):
        providers = settings.get_social_auth_providers(["reddit"])
        app = providers["reddit"]["APP"]
        useragent = (
            '"django:myappid:1.0 (by /u/" + os.environ.get("REDDIT_USERNAME") + ")"'
        )
        assert providers["reddit"]["AUTH_PARAMS"]["duration"] == "permanent"
        assert providers["reddit"]["USER_AGENT"] == useragent
        assert app["client_id"] == 'os.environ.get("REDDIT_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("REDDIT_SECRET")'
        assert app["key"] == 'os.environ.get("REDDIT_KEY")'
        assert providers["reddit"]["SCOPE"] == ["identity"]

    def test_slack(self):
        providers = settings.get_social_auth_providers(["slack"])
        app = providers["slack"]["APP"]
        assert app["client_id"] == 'os.environ.get("SLACK_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("SLACK_SECRET")'
        assert app["key"] == 'os.environ.get("SLACK_KEY")'
        assert providers["slack"]["SCOPE"] == ["read"]

    def test_snapchat(self):
        providers = settings.get_social_auth_providers(["snap"])
        app = providers["snap"]["APP"]
        assert app["client_id"] == 'os.environ.get("SNAPCHAT_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("SNAPCHAT_SECRET")'
        assert app["key"] == 'os.environ.get("SNAPCHAT_KEY")'
        assert providers["snap"]["SCOPE"] == ["read"]

    def test_twitch(self):
        providers = settings.get_social_auth_providers(["twitch"])
        app = providers["twitch"]["APP"]
        assert app["client_id"] == 'os.environ.get("TWITCH_CLIENT_ID")'
        assert app["secret"] == 'os.environ.get("TWITCH_SECRET")'
        assert app["key"] == 'os.environ.get("TWITCH_KEY")'
        assert providers["twitch"]["SCOPE"] == ["read"]
