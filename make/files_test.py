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


def test_replace_in_file_open_file(mock_file):
    files.replace_in_file("test.txt", [(r"in", "out")])
    args = mock_file.call_args_list[0][0]
    assert args[0] == "test.txt"
    assert len(args) == 1


def test_replace_in_file_text(mock_file):
    mock_file().read.return_value = "in"
    files.replace_in_file("test.txt", [(r"in", "out")])
    actual = mock_file().write.call_args[0][0]
    assert actual == "out"


def test_replace_in_file_regex(mock_file):
    mock_file().read.return_value = "in/something\n"
    files.replace_in_file("test.txt", [(r"in\/(.*?)\n", "out")])
    actual = mock_file().write.call_args[0][0]
    assert actual == "out"


def test_replace_in_file_write_file(mock_file):
    files.replace_in_file("test.txt", [(r"in", "out")])
    args = mock_file.call_args_list[1][0]
    assert args[0] == "test.txt"
    assert args[1] == "w"
    assert len(args) == 2


def test_replace_in_file_write_file_dest(mock_file):
    files.replace_in_file("src.txt", [(r"in", "out")], "dest.txt")
    args = mock_file.call_args_list[1][0]
    assert args[0] == "dest.txt"
    assert args[1] == "w"
    assert len(args) == 2


def test_exempt_long_lines_lt(mock_file):
    content = "A" * 87 + "\n"
    mock_file().readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file().writelines.call_args[0][0]
    assert actual == [content]


def test_exempt_long_lines_eq(mock_file):
    content = "A" * 88 + "\n"
    mock_file().readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file().writelines.call_args[0][0]
    assert actual == [content]


def test_exempt_long_lines_gt(mock_file):
    content = "A" * 89 + "\n"
    mock_file().readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file().writelines.call_args[0][0]
    assert actual == ["A" * 89 + "  # noqa: E501\n"]


def test_create_users_model_test_content(mock_file):
    mock_file().read.return_value = "def create_test_user():"
    files.create_users_model_test("users")
    actual = mock_file().write.call_args[0][0]
    assert "def create_test_user():" in actual


def test_create_users_model_test_filename(mock_file):
    files.create_users_model_test("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/models_test.py"
    assert args[1] == "w"


def test_create_users_model_content(mock_file):
    mock_file().read.return_value = "class UserAccount(AbstractUser):"
    files.create_users_model("users")
    actual = mock_file().write.call_args[0][0]
    assert "class UserAccount(AbstractUser):" in actual


def test_create_users_model_filename(mock_file):
    files.create_users_model("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/models.py"
    assert args[1] == "w"


def test_create_users_forms_content(mock_file):
    mock_file().read.return_value = "class UserAccountCreationForm(UserCreationForm):"
    files.create_users_forms("users")
    actual = mock_file().write.call_args[0][0]
    assert "class UserAccountCreationForm(UserCreationForm):" in actual


def test_create_users_forms_filename(mock_file):
    files.create_users_forms("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/forms.py"
    assert args[1] == "w"


def test_create_users_admin_content(mock_file):
    mock_file().read.return_value = "class UserAccountAdmin(UserAdmin):"
    files.create_users_admin("users")
    actual = mock_file().write.call_args[0][0]
    assert "class UserAccountAdmin(UserAdmin):" in actual


def test_create_users_admin_filename(mock_file):
    files.create_users_admin("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/admin.py"
    assert args[1] == "w"


def test_create_base_template_content(mock_file):
    title = "<title>{% block title %}PROJECT{% endblock %}</title>"
    mock_file().read.return_value = title
    files.create_base_template("myproject")
    actual = mock_file().write.call_args[0][0]
    expected = "<title>{% block title %}myproject{% endblock %}</title>"
    assert expected in actual


def test_create_base_template_filename(mock_file):
    files.create_base_template("myproject")
    args = mock_file.call_args[0]
    assert args[0] == "./src/myproject/templates/base.html"
    assert args[1] == "w"


def test_create_home_template_content(mock_file):
    mock_file().read.return_value = "<h1>PROJECT</h1>"
    files.create_home_template("myproject")
    actual = mock_file().write.call_args[0][0]
    expected = "<h1>myproject</h1>"
    assert expected in actual


def test_create_home_template_filename(mock_file):
    files.create_home_template("myproject")
    args = mock_file.call_args[0]
    assert args[0] == "./src/myproject/templates/home.html"
    assert args[1] == "w"


def test_login_template_content(mock_file):
    mock_file().read.return_value = "<h1>Log In</h1>"
    files.create_login_template("users")
    actual = mock_file().write.call_args[0][0]
    expected = "<h1>Log In</h1>"
    assert expected in actual


def test_login_template_filename(mock_file):
    files.create_login_template("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/templates/login.html"
    assert args[1] == "w"


def test_signup_template_content(mock_file):
    mock_file().read.return_value = "<h1>Create an Account</h1>"
    files.create_register_template("users")
    actual = mock_file().write.call_args[0][0]
    expected = "<h1>Create an Account</h1>"
    assert expected in actual


def test_signup_template_filename(mock_file):
    files.create_register_template("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/templates/register.html"
    assert args[1] == "w"


def test_change_cd_workflow_makedirs(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    makedirs_mock = MagicMock()
    monkeypatch.setattr(os, "makedirs", makedirs_mock)
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.change_cd_workflow("myproject", "user")
    makedirs_mock.assert_called_once()


def test_change_cd_workflow_skip_makedirs(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    makedirs_mock = MagicMock()
    monkeypatch.setattr(os, "makedirs", makedirs_mock)
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.change_cd_workflow("myproject", "user")
    makedirs_mock.assert_not_called()


def test_change_cd_workflow_args(monkeypatch):
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


def test_change_readme_write_readme(mock_file):
    files.change_readme("myproject")
    args = mock_file.call_args_list[0][0]
    assert args[0] == "README.md"
    assert args[1] == "w"
    assert len(args) == 2


@pytest.fixture
def change_readme_content(mock_file):
    files.change_readme("myproject")
    return mock_file().write.call_args[0][0]


def test_change_readme_title(change_readme_content):
    actual = change_readme_content
    assert "# myproject\n" in actual


def test_change_readme_link_tdd(change_readme_content):
    actual = change_readme_content
    link = "[test-driven](https://testdriven.io/test-driven-development/)"
    assert link in actual


def test_change_readme_link_cd(change_readme_content):
    actual = change_readme_content
    link = "[continuously deployed](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)"  # noqa: E501
    assert link in actual


def test_change_readme_link_api_first(change_readme_content):
    actual = change_readme_content
    link = "[API-first](https://www.postman.com/api-first/)"
    assert link in actual


def test_change_readme_link_pe(change_readme_content):
    actual = change_readme_content
    link = "[progressively enhanced](https://medium.com/bitsrc/a-practical-guide-to-progressive-enhancement-in-2023-52c740c3aff3)"  # noqa: E501
    assert link in actual


def test_change_readme_link_django(change_readme_content):
    actual = change_readme_content
    link = "[Django](https://www.djangoproject.com/)"
    assert link in actual


@pytest.fixture
def change_scripts_setup(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", mock)
    project_name = "myproject"
    files.change_scripts(project_name)
    return mock, project_name


def test_change_scripts_up(change_scripts_setup):
    mock, project_name = change_scripts_setup
    mock.assert_any_call("up.sh", [("PROJECT", project_name)])


def test_change_scripts_down(change_scripts_setup):
    mock, project_name = change_scripts_setup
    mock.assert_any_call("down.sh", [("PROJECT", project_name)])


def test_change_urls_preserve_imports(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    assert "from django.contrib import admin" in actual


def test_change_urls_import_include(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    assert "from django.urls import include, path" in actual


def test_change_urls_import_template_view(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    assert "from django.views.generic.base import TemplateView" in actual


def test_change_urls_skip_template_view(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject", api_only=True)
    actual = mock_file().write.call_args[0][0]
    assert "from django.views.generic.base import TemplateView" not in actual


def test_change_urls_add_site_name(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    assert 'app_name = "myproject"' in actual


def test_change_urls_preserve_admin_path(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    regex = r"urlpatterns = \[(.*?)path\(\'admin\/\', admin\.site\.urls\),"
    check = re.search(regex, actual, re.DOTALL)
    assert check is not None


def test_change_urls_skip_home(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject", api_only=True)
    actual = mock_file().write.call_args[0][0]
    home = 'path("", TemplateView.as_view(template_name="home.html"), name="home"),'
    assert home not in actual


def test_change_urls_add_home(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    home = 'path("", TemplateView.as_view(template_name="home.html"), name="home"),'
    assert home in actual


def test_change_urls_skip_users_urls(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject", api_only=True)
    actual = mock_file().write.call_args[0][0]
    assert 'path("", include("users.urls")),' not in actual


def test_change_urls_add_users_urls(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    assert 'path("", include("users.urls")),' in actual


def test_change_urls_skip_django_auth_urls(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject", api_only=True)
    actual = mock_file().write.call_args[0][0]
    assert 'path("", include("django.contrib.auth.urls")),' not in actual


def test_change_urls_add_django_auth_urls(mock_file):
    mock_file().read.return_value = urls_py_content
    files.change_urls("myproject")
    actual = mock_file().write.call_args[0][0]
    assert 'path("", include("django.contrib.auth.urls")),' in actual


def test_change_settings_open_file(mock_file):
    mock_file().read.return_value = ""
    files.change_settings("settings.py", "users")
    args = mock_file.call_args_list[1][0]
    assert args[0] == "settings.py"
    assert len(args) == 1


def test_change_settings_write_file(mock_file):
    mock_file().read.return_value = ""
    files.change_settings("settings.py", "users")
    args = mock_file.call_args_list[2][0]
    assert args[0] == "settings.py"
    assert args[1] == "w"
    assert len(args) == 2
