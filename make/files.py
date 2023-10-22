import os
import re

import settings
from django.core.management.utils import get_random_secret_key


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


def create_users_model(users: str):
    content = """from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class UserAccount(AbstractUser):
    pass

    def __str__(self):
      return self.username
"""

    with open(f"./src/{users}/models.py", "w") as file:
        file.write(content)


def create_users_forms(users: str):
    content = """from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class UserAccountCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class UserAccountChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")
"""

    with open(f"./src/{users}/forms.py", "w") as file:
        file.write(content)


def create_users_admin(users: str):
    content = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserAccountCreationForm, UserAccountChangeForm
from .models import UserAccount

class UserAccountAdmin(UserAdmin):
    add_form = UserAccountCreationForm
    form = UserAccountChangeForm
    model = UserAccount
    list_display = ["username"]

admin.site.register(UserAccount, UserAccountAdmin)
"""

    with open(f"./src/{users}/admin.py", "w") as file:
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


def change_pytest_ini(project: str):
    replacements = [
        ("PROJECT", project),
    ]

    replace_in_file("src/pytest.ini", replacements)


def make_env(
    env="prod",
    db="db",
    db_user="db_user",
    db_password="db_password",
    secret_key=get_random_secret_key(),
    debug=0,
):
    replacements = [
        ("DEBUG=1", f"DEBUG={debug}"),
        ("SECRET_KEY=your_secret_key_here", f"SECRET_KEY={secret_key}"),
        ("SQL_DATABASE=myproject_db", f"SQL_DATABASE={db}"),
        ("SQL_USER=django_db_user", f"SQL_USER={db_user}"),
        ("SQL_PASSWORD=password", f"SQL_PASSWORD={db_password}"),
        ("POSTGRES_DB=myproject_db", f"POSTGRES_DB={db}"),
        ("POSTGRES_USER=django_db_user", f"POSTGRES_USER={db_user}"),
        ("POSTGRES_PASSWORD=password", f"POSTGRES_PASSWORD={db_password}"),
    ]

    replace_in_file("docker/.env.example", replacements, dest=f"docker/.env.{env}")


def change_readme(project: str):
    descriptors = [
        ("test-driven", "https://testdriven.io/test-driven-development/"),
        (
            "continuously deployed",
            "https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment",  # noqa: E501
        ),
        ("API-first", "https://www.postman.com/api-first/"),
        (
            "progressively enhanced",
            "https://medium.com/bitsrc/a-practical-guide-to-progressive-enhancement-in-2023-52c740c3aff3",  # noqa: E501
        ),
    ]

    desc = ", ".join([f"[{text}]({url})" for text, url in descriptors])
    django = "[Django](https://www.djangoproject.com/)"
    content = f"# {project}\n\nThis is a {desc} {django} project."

    with open("README.md", "w") as file:
        file.write(content)


def change_scripts(project: str):
    replacements = [
        ("PROJECT", project),
    ]

    replace_in_file("up.sh", replacements)
    replace_in_file("down.sh", replacements)


def change_urls(project: str):
    anchor = "urlpatterns = ["
    app_name = f'app_name = "{project}"'
    replacement = app_name + os.linesep + os.linesep + anchor
    replacements = [
        (r"urlpatterns = \[", replacement),
    ]

    replace_in_file(f"./src/{project}/urls.py", replacements)


def change_settings(filename: str, users: str):
    with open(filename) as file:
        contents = file.read()

    contents = settings.add_installed_apps(contents, users)
    contents = settings.change_database_settings(contents)
    contents = settings.add_new_settings(contents, users)
    contents = settings.add_import_os(contents)
    contents = settings.set_secret_key(contents)
    contents = settings.set_debug(contents)
    contents = settings.set_allowed_hosts(contents)
    contents = settings.add_prod_rest_framework_renderer(contents)

    with open(filename, "w") as file:
        file.write(contents)
