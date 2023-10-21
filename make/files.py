import os
import re


def replace_in_file(src: str, replacements, dest=None):
    if dest is None:
        dest = src

    with open(src) as file:
        contents = file.read()

    for pattern, repl in replacements:
        contents = re.sub(pattern, repl, contents)

    with open(dest, "w") as file:
        file.write(contents)


def exempt_long_lines(filename: str):
    with open(filename) as file:
        lines = file.readlines()

    modified_lines = [
        line.rstrip() + "  # noqa: E501\n"
        if len(line.rstrip()) > 88
        else line.rstrip() + "\n"
        for line in lines
    ]

    with open(filename, "w") as file:
        file.writelines(modified_lines)


def create_users_model_tests(users: str):
    content = """import pytest
import datetime
from django.utils import timezone
from .models import UserAccount


@pytest.mark.django_db
def test_active_default():
    account = UserAccount()
    assert account.is_active is True


@pytest.mark.django_db
def test_created_default():
    before = timezone.now()
    account = UserAccount()
    after = timezone.now()
    assert isinstance(account.created, datetime.datetime)
    assert before <= account.created
    assert after >= account.created
"""

    with open(f"./src/{users}/models_test.py", "w") as file:
        file.write(content)


def create_users_model(users: str):
    content = """from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone


class UserAccount(AbstractBaseUser):
    username = models.TextField(blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "is_active",
    ]
"""

    with open(f"./src/{users}/models.py", "w") as file:
        file.write(content)


def change_cd_workflow(project: str, droplet_user: str):
    workflow_directory = "./.github/workflows"
    if not os.path.exists(workflow_directory):
        os.makedirs(workflow_directory)

    replacements = [
        ("PROJECT", project),
        ("DEPLOYER_USERNAME", droplet_user),
    ]

    replace_in_file("cd.yml", replacements, dest="./.github/workflows/cd.yml")


def change_dockerfile(project: str):
    replacements = [
        ('ARG SITENAME="django_starter"', f'ARG SITENAME="{project}"'),
    ]

    replace_in_file("docker/Dockerfile", replacements)


def change_compose_prod(repo: str, deployer: str, env: str):
    replacements = [
        ("image: ghcr.io/REPO:main", f"image: ghcr.io/{repo}:main"),
        ("- /home/deployer/.env.prod", f"- /home/{deployer}/.env.prod"),
    ]

    replace_in_file(f"docker/docker-compose.{env}.yml", replacements)
