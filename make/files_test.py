import os
from unittest.mock import MagicMock, mock_open

import files
import pytest

urls_py_content = """from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
"""


@pytest.fixture
def mock_file(monkeypatch):
    mock = mock_open()
    monkeypatch.setattr("builtins.open", mock)
    return mock


class TestReplaceInFile:
    def test_open_file(self, mock_file):
        files.replace_in_file("test.txt", [(r"in", "out")])
        args = mock_file.call_args_list[0][0]
        assert args[0] == "test.txt"
        assert len(args) == 1

    def test_text(self, mock_file):
        mock_file().read.return_value = "in"
        files.replace_in_file("test.txt", [(r"in", "out")])
        actual = mock_file().write.call_args[0][0]
        assert actual == "out"

    def test_regex(self, mock_file):
        mock_file().read.return_value = "in/something\n"
        files.replace_in_file("test.txt", [(r"in\/(.*?)\n", "out")])
        actual = mock_file().write.call_args[0][0]
        assert actual == "out"

    def test_write_file(self, mock_file):
        files.replace_in_file("test.txt", [(r"in", "out")])
        args = mock_file.call_args_list[1][0]
        assert args[0] == "test.txt"
        assert args[1] == "w"
        assert len(args) == 2

    def test_write_file_dest(self, mock_file):
        files.replace_in_file("src.txt", [(r"in", "out")], "dest.txt")
        args = mock_file.call_args_list[1][0]
        assert args[0] == "dest.txt"
        assert args[1] == "w"
        assert len(args) == 2


class TestExemptLongLines:
    def test_less_than(self, mock_file):
        content = "A" * 87 + "\n"
        mock_file().readlines.return_value = [content]
        files.exempt_long_lines("test.txt")
        actual = mock_file().writelines.call_args[0][0]
        assert actual == [content]

    def test_equal_to(self, mock_file):
        content = "A" * 88 + "\n"
        mock_file().readlines.return_value = [content]
        files.exempt_long_lines("test.txt")
        actual = mock_file().writelines.call_args[0][0]
        assert actual == [content]

    def test_greater_than(self, mock_file):
        content = "A" * 89 + "\n"
        mock_file().readlines.return_value = [content]
        files.exempt_long_lines("test.txt")
        actual = mock_file().writelines.call_args[0][0]
        assert actual == ["A" * 89 + "  # noqa: E501\n"]


class TestCreateBaseTemplate:
    def test_content(self, mock_file):
        title = "<title>{% block title %}PROJECT{% endblock %}</title>"
        mock_file().read.return_value = title
        files.create_base_template("myproject")
        actual = mock_file().write.call_args[0][0]
        expected = "<title>{% block title %}myproject{% endblock %}</title>"
        assert expected in actual

    def test_filename(self, mock_file):
        files.create_base_template("myproject")
        args = mock_file.call_args[0]
        assert args[0] == "./src/myproject/templates/base.html"
        assert args[1] == "w"


class TestCreateHomeTemplate:
    def test_content(self, mock_file):
        mock_file().read.return_value = "<h1>PROJECT</h1>"
        files.create_home_template("myproject")
        actual = mock_file().write.call_args[0][0]
        expected = "<h1>myproject</h1>"
        assert expected in actual

    def test_filename(self, mock_file):
        files.create_home_template("myproject")
        args = mock_file.call_args[0]
        assert args[0] == "./src/myproject/templates/home.html"
        assert args[1] == "w"


class TestChangeCDWorkflow:
    def test_makedirs(self, monkeypatch):
        monkeypatch.setattr(os.path, "exists", lambda _: False)
        makedirs_mock = MagicMock()
        monkeypatch.setattr(os, "makedirs", makedirs_mock)
        replace_in_file_mock = MagicMock()
        monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
        files.change_cd_workflow("myproject", "user")
        makedirs_mock.assert_called_once()

    def test_skip_makedirs(self, monkeypatch):
        monkeypatch.setattr(os.path, "exists", lambda _: True)
        makedirs_mock = MagicMock()
        monkeypatch.setattr(os, "makedirs", makedirs_mock)
        replace_in_file_mock = MagicMock()
        monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
        files.change_cd_workflow("myproject", "user")
        makedirs_mock.assert_not_called()

    def test_args(self, monkeypatch):
        monkeypatch.setattr(os.path, "exists", lambda _: True)
        monkeypatch.setattr(os, "makedirs", lambda _: None)
        replace_in_file_mock = MagicMock()
        monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
        files.change_cd_workflow("myproject", "user")
        replace_in_file_mock.assert_called_once_with(
            "cd.yml",
            [("PROJECT", "myproject"), ("DEPLOYER_USERNAME", "user")],
            dest="./.github/workflows/cd.yml",
        )


def test_change_dockerfile_args(monkeypatch):
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.change_dockerfile("myproject")
    replace_in_file_mock.assert_called_once_with(
        "docker/Dockerfile",
        [('ARG SITENAME="django_starter"', 'ARG SITENAME="myproject"')],
    )


def test_change_compose_prod_args(monkeypatch):
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.change_compose_prod("repo", "deployer", "prod")
    replace_in_file_mock.assert_called_once_with(
        "docker/docker-compose.prod.yml",
        [
            ("image: ghcr.io/REPO:main", "image: ghcr.io/repo:main"),
            ("- /home/deployer/.env.prod", "- /home/deployer/.env.prod"),
        ],
    )


def test_change_pytest_ini_args(monkeypatch):
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    project_name = "myproject"
    files.change_pytest_ini(project_name)
    replace_in_file_mock.assert_called_once_with(
        "src/.pytest.ini", [("PROJECT", project_name)], dest="src/pytest.ini"
    )


def test_make_env_args(monkeypatch):
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.make_env(env="env", secret_key="test", debug=1)
    replace_in_file_mock.assert_called_once_with(
        "docker/.env.example",
        [
            ("DEBUG=1", "DEBUG=1"),
            ("SECRET_KEY=your_secret_key_here", "SECRET_KEY=test"),
        ],
        dest="docker/.env.env",
    )


class TestChangeReadme:
    @pytest.fixture
    def change_readme_content(self, mock_file):
        files.change_readme("myproject")
        return mock_file().write.call_args[0][0]

    def test_readme(self, mock_file):
        files.change_readme("myproject")
        args = mock_file.call_args_list[0][0]
        assert args[0] == "README.md"
        assert args[1] == "w"
        assert len(args) == 2

    def test_title(self, change_readme_content):
        actual = change_readme_content
        assert "# myproject\n" in actual

    def test_link_tdd(self, change_readme_content):
        actual = change_readme_content
        link = "[test-driven](https://testdriven.io/test-driven-development/)"
        assert link in actual

    def test_link_cd(self, change_readme_content):
        actual = change_readme_content
        link = "[continuously deployed](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)"  # noqa: E501
        assert link in actual

    def test_link_api_first(self, change_readme_content):
        actual = change_readme_content
        link = "[API-first](https://www.postman.com/api-first/)"
        assert link in actual

    def test_link_pe(self, change_readme_content):
        actual = change_readme_content
        link = "[progressively enhanced](https://medium.com/bitsrc/a-practical-guide-to-progressive-enhancement-in-2023-52c740c3aff3)"  # noqa: E501
        assert link in actual

    def test_link_django(self, change_readme_content):
        actual = change_readme_content
        link = "[Django](https://www.djangoproject.com/)"
        assert link in actual


class TestChangeScripts:
    @pytest.fixture
    def setup(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(files, "replace_in_file", mock)
        project_name = "myproject"
        files.change_scripts(project_name)
        return mock, project_name

    def test_up(self, setup):
        mock, project_name = setup
        mock.assert_any_call("up.sh", [("PROJECT", project_name)])

    def test_down(self, setup):
        mock, project_name = setup
        mock.assert_any_call("down.sh", [("PROJECT", project_name)])


class TestChangeURLs:
    @pytest.fixture
    def contents(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        return mock_file().write.call_args[0][0]

    @pytest.fixture
    def contents_api_only(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject", api_only=True)
        return mock_file().write.call_args[0][0]

    def test_preserve_imports(self, contents):
        assert "from django.contrib import admin" in contents

    def test_import_include(self, contents):
        assert "from django.urls import include, path" in contents

    def test_import_template_view(self, contents):
        assert "from django.views.generic.base import TemplateView" in contents

    def test_skip_template_view(self, contents_api_only):
        statement = "from django.views.generic.base import TemplateView"
        assert statement not in contents_api_only

    def test_import_settings(self, contents):
        assert "from django.conf import settings" in contents

    def test_import_rest_framework(self, contents):
        assert "from rest_framework import permissions" in contents

    def test_import_drf_yasg_views(self, contents):
        assert "from drf_yasg.views import get_schema_view" in contents

    def test_import_drf_yasg(self, contents):
        assert "from drf_yasg import openapi" in contents

    def test_add_app_name(self, contents):
        assert 'app_name = "myproject"' in contents

    def test_add_api_variable(self, contents):
        assert "api = settings.API_BASE" in contents

    def test_add_schema_view(self, contents):
        expected = """schema_view = get_schema_view(
    openapi.Info(
        title="myproject API",
        default_version="v1",
        description="API for myproject",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)"""
        assert expected in contents

    def test_preserve_admin_path(self, contents):
        assert 'path("admin/", admin.site.urls),' in contents

    def test_skip_home(self, contents_api_only):
        home = 'path("", TemplateView.as_view(template_name="home.html"), name="home"),'
        assert home not in contents_api_only

    def test_add_home(self, contents):
        home = 'path("", TemplateView.as_view(template_name="home.html"), name="home"),'
        assert home in contents

    def test_skip_users_urls(self, contents_api_only):
        assert 'path("", include("users.urls")),' not in contents_api_only

    def test_add_users_urls(self, contents):
        assert 'path("", include("users.urls")),' in contents

    def test_skip_django_auth_urls(self, contents_api_only):
        path = 'path("", include("django.contrib.auth.urls")),'
        assert path not in contents_api_only

    def test_add_django_auth_urls(self, contents):
        assert 'path("", include("django.contrib.auth.urls")),' in contents

    def test_schema_json(self, contents):
        expected = """path(
        f"{api}/doc<format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),"""
        assert expected in contents

    def test_schema_swagger_ui(self, contents):
        expected = """path(
        f"{api}/doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),"""
        assert expected in contents

    def test_schema_redoc(self, contents):
        expected = """path(
        f"{api}/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),"""
        assert expected in contents


class TestChangeSettings:
    def test_read_file(self, mock_file):
        mock_file().read.return_value = ""
        files.change_settings("settings.py", "users")
        args = mock_file.call_args_list[1][0]
        assert args[0] == "settings.py"
        assert len(args) == 1

    def test_write_file(self, mock_file):
        mock_file().read.return_value = ""
        files.change_settings("settings.py", "users")
        args = mock_file.call_args_list[2][0]
        assert args[0] == "settings.py"
        assert args[1] == "w"
        assert len(args) == 2


class TestCopyFiles:
    @pytest.fixture
    def calls(self, mock_file):
        files.copy_files("myproject", "usersapp")
        return [str(call_[0]) for call_ in mock_file.call_args_list]

    @pytest.fixture
    def api_only_calls(self, mock_file):
        files.copy_files("myproject", "usersapp", api_only=True)
        return [str(call_[0]) for call_ in mock_file.call_args_list]

    def test_read_conftest(self, calls):
        assert "('make/.conftest.py',)" in calls

    def test_write_conftest(self, calls):
        assert "('./src/conftest.py', 'w')" in calls

    def test_read_testsh(self, calls):
        assert "('make/test.sh',)" in calls

    def test_write_testsh(self, calls):
        assert "('./src/test.sh', 'w')" in calls

    def test_read_400_template(self, calls):
        assert "('make/templates/400.html',)" in calls

    def test_write_400_template(self, calls):
        assert "('./src/myproject/templates/400.html', 'w')" in calls

    def test_read_403_template(self, calls):
        assert "('make/templates/403.html',)" in calls

    def test_write_403_template(self, calls):
        assert "('./src/myproject/templates/403.html', 'w')" in calls

    def test_read_404_template(self, calls):
        assert "('make/templates/404.html',)" in calls

    def test_write_404_template(self, calls):
        assert "('./src/myproject/templates/404.html', 'w')" in calls

    def test_read_500_template(self, calls):
        assert "('make/templates/500.html',)" in calls

    def test_write_500_template(self, calls):
        assert "('./src/myproject/templates/500.html', 'w')" in calls

    def test_read_users_admin(self, calls):
        assert "('make/users/admin.py',)" in calls

    def test_write_users_admin(self, calls):
        assert "('./src/usersapp/admin.py', 'w')" in calls

    def test_read_users_forms(self, calls):
        assert "('make/users/forms.py',)" in calls

    def test_write_users_forms(self, calls):
        assert "('./src/usersapp/forms.py', 'w')" in calls

    def test_read_users_models(self, calls):
        assert "('make/users/models.py',)" in calls

    def test_write_users_models(self, calls):
        assert "('./src/usersapp/models.py', 'w')" in calls

    def test_read_users_models_tests(self, calls):
        assert "('make/users/models.test.py',)" in calls

    def test_write_users_models_tests(self, calls):
        assert "('./src/usersapp/models_test.py', 'w')" in calls

    def test_read_users_serializers(self, calls):
        assert "('make/users/serializers.py',)" in calls

    def test_write_users_serializers(self, calls):
        assert "('./src/usersapp/serializers.py', 'w')" in calls

    def test_read_users_serializers_tests(self, calls):
        assert "('make/users/serializers.test.py',)" in calls

    def test_write_users_serializers_tests(self, calls):
        assert "('./src/usersapp/serializers_test.py', 'w')" in calls

    def test_read_users_urls(self, calls):
        assert "('make/users/urls.py',)" in calls

    def test_write_users_urls(self, calls):
        assert "('./src/usersapp/urls.py', 'w')" in calls

    def test_read_users_views(self, calls):
        assert "('make/users/views.py',)" in calls

    def test_write_users_views(self, calls):
        assert "('./src/usersapp/views.py', 'w')" in calls

    def test_read_users_views_tests(self, calls):
        assert "('make/users/views.test.py',)" in calls

    def test_write_users_views_tests(self, calls):
        assert "('./src/usersapp/views_test.py', 'w')" in calls

    def test_read_login_template(self, calls):
        assert "('make/users/templates/login.html',)" in calls

    def test_write_login_template(self, calls):
        assert "('./src/usersapp/templates/login.html', 'w')" in calls

    def test_read_register_template(self, calls):
        assert "('make/users/templates/register.html',)" in calls

    def test_write_register_template(self, calls):
        assert "('./src/usersapp/templates/register.html', 'w')" in calls

    def test_no_read_users_api_only_urls(self, api_only_calls):
        assert "('make/users/urls.py',)" not in api_only_calls

    def test_read_users_api_only_urls(self, api_only_calls):
        assert "('make/users/urls.api-only.py',)" in api_only_calls

    def test_write_users_api_only_urls(self, api_only_calls):
        assert "('./src/usersapp/urls.py', 'w')" in api_only_calls


def test_add_provider_env(mock_file):
    mock_file().read.return_value = ""
    providers = [
        "apple",
        "auth0",
        "digitalocean",
        "discord",
        "facebook",
        "github",
        "google",
        "instagram",
        "linkedin",
        "patreon",
        "reddit",
        "slack",
        "snap",
        "twitch",
    ]
    files.add_provider_env(providers)
    actual = mock_file().write.call_args[0][0]

    assert "APPLE_CLIENT_ID=" in actual
    assert "APPLE_SECRET=" in actual
    assert "APPLE_KEY=" in actual
    assert "APPLE_CERTIFICATE_KEY=" in actual

    assert "AUTH0_CLIENT_ID=" in actual
    assert "AUTH0_SECRET=" in actual
    assert "AUTH0_KEY=" in actual
    assert "AUTH0_URL=" in actual

    assert "DIGITALOCEAN_CLIENT_ID=" in actual
    assert "DIGITALOCEAN_SECRET=" in actual
    assert "DIGITALOCEAN_KEY=" in actual

    assert "DISCORD_CLIENT_ID=" in actual
    assert "DISCORD_SECRET=" in actual
    assert "DISCORD_KEY=" in actual

    assert "FACEBOOK_CLIENT_ID=" in actual
    assert "FACEBOOK_SECRET=" in actual
    assert "FACEBOOK_KEY=" in actual

    assert "GITHUB_CLIENT_ID=" in actual
    assert "GITHUB_SECRET=" in actual
    assert "GITHUB_KEY=" in actual

    assert "GOOGLE_CLIENT_ID=" in actual
    assert "GOOGLE_SECRET=" in actual
    assert "GOOGLE_KEY=" in actual

    assert "INSTAGRAM_CLIENT_ID=" in actual
    assert "INSTAGRAM_SECRET=" in actual
    assert "INSTAGRAM_KEY=" in actual

    assert "LINKEDIN_CLIENT_ID=" in actual
    assert "LINKEDIN_SECRET=" in actual
    assert "LINKEDIN_KEY=" in actual

    assert "PATREON_CLIENT_ID=" in actual
    assert "PATREON_SECRET=" in actual
    assert "PATREON_KEY=" in actual

    assert "REDDIT_CLIENT_ID=" in actual
    assert "REDDIT_SECRET=" in actual
    assert "REDDIT_KEY=" in actual
    assert "REDDIT_USERNAME=" in actual

    assert "SLACK_CLIENT_ID=" in actual
    assert "SLACK_SECRET=" in actual
    assert "SLACK_KEY=" in actual

    assert "SNAPCHAT_CLIENT_ID=" in actual
    assert "SNAPCHAT_SECRET=" in actual
    assert "SNAPCHAT_KEY=" in actual

    assert "TWITCH_CLIENT_ID=" in actual
    assert "TWITCH_SECRET=" in actual
    assert "TWITCH_KEY=" in actual


class TestMakeNext:
    @pytest.fixture
    def mock(self, mock_file):
        mock_file().read.side_effect = ["One", "Two", "Three", "Four", "Five"]
        return mock_file

    @staticmethod
    def provider_read(provider, mock):
        files.make_next([provider])
        args = mock.call_args_list[2]
        assert args[0] == (f"./next/{provider}.md",)

    @staticmethod
    def provider_write(provider, mock):
        files.make_next([provider])
        args = mock.call_args_list[4]
        text = mock().write.call_args[0][0]
        assert args[0] == ("./NEXT.md", "w")
        assert "Two" in text

    def test_read_1(self, mock):
        files.make_next([])
        args = mock.call_args_list[1]
        assert args[0] == ("./next/1.md",)

    def test_write_1(self, mock):
        files.make_next([])
        args = mock.call_args_list[3]
        text = mock().write.call_args[0][0]
        assert args[0] == ("./NEXT.md", "w")
        assert "One" in text

    def test_read_apple(self, mock):
        self.provider_read("apple", mock)

    def test_write_apple(self, mock):
        self.provider_write("apple", mock)

    def test_read_auth0(self, mock):
        self.provider_read("auth0", mock)

    def test_write_auth0(self, mock):
        self.provider_write("auth0", mock)

    def test_read_digitalocean(self, mock):
        self.provider_read("digitalocean", mock)

    def test_write_digitalocean(self, mock):
        self.provider_write("digitalocean", mock)

    def test_read_discord(self, mock):
        self.provider_read("discord", mock)

    def test_write_discord(self, mock):
        self.provider_write("discord", mock)

    def test_read_facebook(self, mock):
        self.provider_read("facebook", mock)

    def test_write_facebook(self, mock):
        self.provider_write("facebook", mock)

    def test_read_github(self, mock):
        self.provider_read("github", mock)

    def test_write_github(self, mock):
        self.provider_write("github", mock)

    def test_read_google(self, mock):
        self.provider_read("google", mock)

    def test_write_google(self, mock):
        self.provider_write("google", mock)

    def test_read_instagram(self, mock):
        self.provider_read("instagram", mock)

    def test_write_instagram(self, mock):
        self.provider_write("instagram", mock)

    def test_read_linkedin(self, mock):
        self.provider_read("linkedin", mock)

    def test_write_linkedin(self, mock):
        self.provider_write("linkedin", mock)

    def test_read_patreon(self, mock):
        self.provider_read("patreon", mock)

    def test_write_patreon(self, mock):
        self.provider_write("patreon", mock)

    def test_read_reddit(self, mock):
        self.provider_read("reddit", mock)

    def test_write_reddit(self, mock):
        self.provider_write("reddit", mock)

    def test_read_slack(self, mock):
        self.provider_read("slack", mock)

    def test_write_slack(self, mock):
        self.provider_write("slack", mock)

    def test_read_snap(self, mock):
        self.provider_read("snap", mock)

    def test_write_snap(self, mock):
        self.provider_write("snap", mock)

    def test_read_twitch(self, mock):
        self.provider_read("twitch", mock)

    def test_write_twitch(self, mock):
        self.provider_write("twitch", mock)

    def test_read_2(self, mock):
        files.make_next([])
        args = mock.call_args_list[2]
        assert args[0] == ("./next/2.md",)

    def test_write_2(self, mock):
        files.make_next([])
        args = mock.call_args_list[3]
        text = mock().write.call_args[0][0]
        assert args[0] == ("./NEXT.md", "w")
        assert "Two" in text
