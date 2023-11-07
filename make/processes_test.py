import subprocess

import processes
import pytest


class TestCreateDjangoProject:
    @pytest.fixture
    def setup(self, monkeypatch):
        run_args = None

        def mock_run(*args, **kwargs):
            nonlocal run_args
            run_args = (args, kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)
        test_project_name = "myproject"
        processes.create_django_project(test_project_name)
        return run_args, test_project_name

    def test_command(self, setup):
        run_args, test_project_name = setup
        assert run_args[0][0] == [
            "django-admin",
            "startproject",
            test_project_name,
            ".",
        ]

    def test_cwd(self, setup):
        run_args, _ = setup
        assert run_args[1]["cwd"] == "src"


class TestCreateUsersApp:
    @pytest.fixture
    def setup(self, monkeypatch):
        run_args = None

        def mock_run(*args, **kwargs):
            nonlocal run_args
            run_args = (args, kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)
        test_app_name = "users"
        processes.create_users_app(test_app_name)
        return run_args, test_app_name

    def test_command(self, setup):
        run_args, test_app_name = setup
        assert run_args[0][0] == ["python", "manage.py", "startapp", test_app_name]

    def test_cwd(self, setup):
        run_args, _ = setup
        assert run_args[1]["cwd"] == "src"


class TestCreateTemplatesDir:
    @pytest.fixture
    def setup(self, monkeypatch):
        run_args = None

        def mock_run(*args, **kwargs):
            nonlocal run_args
            run_args = (args, kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)
        test_project_name = "myproject"
        processes.create_templates_dir(test_project_name)
        return run_args, test_project_name

    def test_command(self, setup):
        run_args, test_project_name = setup
        expected = f"{test_project_name}/templates/registration"
        assert run_args[0][0] == ["mkdir", "-p", expected]

    def test_cwd(self, setup):
        run_args, _ = setup
        assert run_args[1]["cwd"] == "src"
