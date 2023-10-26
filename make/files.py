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


def create_users_model_test(users: str):
    dest = f"./src/{users}/models_test.py"
    replace_in_file("make/users/models_test.py", [], dest=dest)


def create_users_model(users: str):
    replace_in_file("make/users/models.py", [], dest=f"./src/{users}/models.py")


def create_users_forms(users: str):
    replace_in_file("make/users/forms.py", [], dest=f"./src/{users}/forms.py")


def create_users_admin(users: str):
    replace_in_file("make/users/admin.py", [], dest=f"./src/{users}/admin.py")


def create_base_template(project: str):
    replacements = [(r"PROJECT", project)]
    src = "make/templates/base.html"
    dest = f"./src/{project}/templates/base.html"
    replace_in_file(src, replacements, dest=dest)


def create_home_template(project: str):
    replacements = [(r"PROJECT", project)]
    src = "make/templates/home.html"
    dest = f"./src/{project}/templates/home.html"
    replace_in_file(src, replacements, dest=dest)


def create_login_template(users: str):
    src = "make/users/templates/login.html"
    dest = f"./src/{users}/templates/login.html"
    replace_in_file(src, [], dest=dest)


def create_register_template(users: str):
    src = "make/users/templates/register.html"
    dest = f"./src/{users}/templates/register.html"
    replace_in_file(src, [], dest=dest)


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


def change_settings(filename: str, users: str, api_only: bool = False):
    with open(filename) as file:
        contents = file.read()

    contents = settings.add_installed_apps(contents, users)
    contents = settings.change_database_settings(contents)
    contents = settings.add_new_settings(contents, users, api_only=api_only)
    contents = settings.add_import_os(contents)
    contents = settings.set_secret_key(contents)
    contents = settings.set_debug(contents)
    contents = settings.set_allowed_hosts(contents)
    contents = settings.add_prod_rest_framework_renderer(contents)

    with open(filename, "w") as file:
        file.write(contents)
