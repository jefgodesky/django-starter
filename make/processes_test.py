import subprocess

import processes
import pytest


@pytest.fixture
def create_django_project_setup(monkeypatch):
    run_args = None

    def mock_run(*args, **kwargs):
        nonlocal run_args
        run_args = (args, kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)
    test_project_name = "myproject"
    processes.create_django_project(test_project_name)
    return run_args, test_project_name


def test_create_django_project_command(create_django_project_setup):
    run_args, test_project_name = create_django_project_setup
    assert run_args[0][0] == ["django-admin", "startproject", test_project_name, "."]


def test_create_django_project_cwd(create_django_project_setup):
    run_args, _ = create_django_project_setup
    assert run_args[1]["cwd"] == "src"
