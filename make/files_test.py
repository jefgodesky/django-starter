import os
import re
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
        "src/pytest.ini",
        [("PROJECT", project_name)],
    )


def test_make_env_args(monkeypatch):
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.make_env(
        env="env",
        db="db",
        db_user="db_user",
        db_password="db_password",
        secret_key="test",
        debug=1,
    )
    replace_in_file_mock.assert_called_once_with(
        "docker/.env.example",
        [
            ("DEBUG=1", "DEBUG=1"),
            ("SECRET_KEY=your_secret_key_here", "SECRET_KEY=test"),
            ("SQL_DATABASE=myproject_db", "SQL_DATABASE=db"),
            ("SQL_USER=django_db_user", "SQL_USER=db_user"),
            ("SQL_PASSWORD=password", "SQL_PASSWORD=db_password"),
            ("POSTGRES_DB=myproject_db", "POSTGRES_DB=db"),
            ("POSTGRES_USER=django_db_user", "POSTGRES_USER=db_user"),
            ("POSTGRES_PASSWORD=password", "POSTGRES_PASSWORD=db_password"),
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
    def test_preserve_imports(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        assert "from django.contrib import admin" in actual

    def test_import_include(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        assert "from django.urls import include, path" in actual

    def test_import_template_view(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        assert "from django.views.generic.base import TemplateView" in actual

    def test_skip_template_view(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject", api_only=True)
        actual = mock_file().write.call_args[0][0]
        assert "from django.views.generic.base import TemplateView" not in actual

    def test_add_site_name(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        assert 'app_name = "myproject"' in actual

    def test_preserve_admin_path(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        regex = r"urlpatterns = \[(.*?)path\(\'admin\/\', admin\.site\.urls\),"
        check = re.search(regex, actual, re.DOTALL)
        assert check is not None

    def test_skip_home(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject", api_only=True)
        actual = mock_file().write.call_args[0][0]
        home = 'path("", TemplateView.as_view(template_name="home.html"), name="home"),'
        assert home not in actual

    def test_add_home(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        home = 'path("", TemplateView.as_view(template_name="home.html"), name="home"),'
        assert home in actual

    def test_skip_users_urls(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject", api_only=True)
        actual = mock_file().write.call_args[0][0]
        assert 'path("", include("users.urls")),' not in actual

    def test_add_users_urls(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        assert 'path("", include("users.urls")),' in actual

    def test_skip_django_auth_urls(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject", api_only=True)
        actual = mock_file().write.call_args[0][0]
        assert 'path("", include("django.contrib.auth.urls")),' not in actual

    def test_add_django_auth_urls(self, mock_file):
        mock_file().read.return_value = urls_py_content
        files.change_urls("myproject")
        actual = mock_file().write.call_args[0][0]
        assert 'path("", include("django.contrib.auth.urls")),' in actual


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
