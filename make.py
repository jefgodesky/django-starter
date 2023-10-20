import os
import re
import subprocess
from inspect import cleandoc

from django.core.management.utils import get_random_secret_key
from git import Repo


def print_bold(msg: str):
    print("\033[1m" + msg + "\033[0m")


def print_intro():
    title = "Let’s start a new Django project!"
    intro = """This script will help you get set up for a new Django project. It’s quite
      opinionated, though. If you’re interested in running a Dockerized, API-first
      Django site using test-driven development (TDD) and continuous delivery (CD)
      to a Digital Ocean droplet, then this script will give you a great starting
      point. If you’re looking for something else, then I’m afraid this script won’t
      be of much help to you. Godspeed on your journey, friend. But if that is what
      you’re looking for, well, let’s get started!"""
    print_bold(title)
    print(cleandoc(intro))


def prompt(msg: str, prompt_text: str):
    print("\n" + msg)
    return input(prompt_text)


def get_project(default_value: str):
    msg = "What would you like to call your project?"
    prompt_text = f"Project name ({default_value}): "
    return prompt(msg, prompt_text) or default_value


def get_repo(default_value: str):
    msg = "What is the name of your Github repository?"
    prompt_text = f"Repository ({default_value}): "
    return prompt(msg, prompt_text) or default_value


def get_deployer():
    msg = """You’ll want to create a non-root user on your DigitalOcean droplet
      who has all the permissions it needs to deploy your Docker containers.
      This should be an account separate from any human user, one dedicated entirely
      to automated, continuous delivery. What is this user’s user name?"""
    prompt_text = "Deployment username: "
    return prompt(cleandoc(msg), prompt_text)


def get_users_appname():
    msg = "What would you like to call the app that handles your users?"
    prompt_text = "Users app (users): "
    return prompt(cleandoc(msg), prompt_text) or "users"


def get_database(env: str):
    msg_before = "What is the name of the database that you would like to use in your "
    msg = f"{msg_before} {env} environment?"
    prompt_text = f"{env.capitalize()} database: "
    return prompt(cleandoc(msg), prompt_text)


def get_database_user(env: str):
    msg_before = "What is the name of the database user for your "
    msg = f"{msg_before} {env} environment database?"
    prompt_text = f"{env.capitalize()} database user: "
    return prompt(cleandoc(msg), prompt_text)


def get_database_password(env: str):
    msg_before = "What is the password for the database user for your "
    msg = f"{msg_before} {env} environment database?"
    prompt_text = f"{env.capitalize()} database user password: "
    return prompt(cleandoc(msg), prompt_text)


def create_django_project(project: str):
    subprocess.run(["django-admin", "startproject", project, "."], cwd="src")


def create_users_app(users: str):
    subprocess.run(["python", "manage.py", "startapp", users], cwd="src")


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


def add_installed_apps(settings: str, users: str):
    apps_to_add = ['"rest_framework"', users]
    match = re.search(r"INSTALLED_APPS = \[(.*?)]", settings, flags=re.DOTALL)
    if not match:
        return settings
    apps_existing_str = match.group(1).strip()
    apps_existing = [app.strip() for app in apps_existing_str.split(",") if app]
    apps = apps_existing + apps_to_add
    apps_str = ",\n    ".join(apps)
    installed_str = f"INSTALLED_APPS = [\n    {apps_str},\n]"
    return settings.replace(match.group(0), installed_str)


def change_database_settings(settings: str):
    match_databases = re.search(r"DATABASES = {[^}]*}", settings, flags=re.DOTALL)
    if not match_databases:
        return settings
    databases = """{
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
"""
    return settings.replace(match_databases.group(0), f"DATABASES = {databases}")


def change_settings(filename: str, users: str):
    with open(filename) as file:
        settings = file.read()

    settings = add_installed_apps(settings, users)
    settings = change_database_settings(settings)

    new_settings_anchor = "from pathlib import Path"
    new_settings = [f'AUTH_USER_MODEL = "{users}.UserAccount"', "SITE_ID = 1"]
    new_settings_string = (
        os.linesep + os.linesep + os.linesep.join(new_settings) + os.linesep
    )

    replacements = [
        (new_settings_anchor, new_settings_anchor + new_settings_string),
        (r"from pathlib import Path", "import os\nfrom pathlib import Path"),
        (r'SECRET_KEY = "(.*)"', 'SECRET_KEY = os.environ.get("SECRET_KEY")'),
        (r"DEBUG = True", 'DEBUG = int(os.environ.get("DEBUG", default=0))'),
        (
            r"ALLOWED_HOSTS = \[\]",
            'ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")',
        ),
    ]

    for pattern, repl in replacements:
        settings = re.sub(pattern, repl, settings)

    settings = (
        settings
        + """

if not DEBUG:
    REST_FRAMEWORK = {
        "DEFAULT_RENDERER_CLASSES": "rest_framework.renderers.JSONRenderer"
    }
"""
    )

    with open(filename, "w") as file:
        file.write(settings)


def create_users_model(users: str):
    lines = [
        "from django.contrib.auth.models import AbstractBaseUser",
        "from django.db import models",
        "from django.utils import timezone",
        "",
        "",
        "class UserAccount(AbstractBaseUser):",
        "    username = models.TextField(blank=False, unique=True)",
        "    is_active = models.BooleanField(default=True)",
        "",
        '    USERNAME_FIELD = "username"',
        "    REQUIRED_FIELDS = [",
        '        "is_active",',
        "    ]",
    ]

    with open(f"./src/{users}/models.py", "w") as file:
        file.write(os.linesep.join(lines))


def replace_in_file(src: str, replacements, dest=None):
    if dest is None:
        dest = src

    with open(src) as file:
        contents = file.read()

    for pattern, repl in replacements:
        contents = re.sub(pattern, repl, contents)

    with open(dest, "w") as file:
        file.write(contents)


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


def change_compose_prod(repo: str, deployer: str):
    replacements = [
        ("image: ghcr.io/REPO:main", f"image: ghcr.io/{repo}:main"),
        ("- /home/deployer/.env.prod", f"- /home/{deployer}/.env.prod"),
    ]

    replace_in_file("docker/docker-compose.prod.yml", replacements)


def change_pytest_ini(project: str):
    replacements = [
        ("PROJECT", project),
    ]

    replace_in_file("src/pytest.ini", replacements)


def make_env(env: str, db: str, db_user: str, db_password: str):
    debug_environments = ["dev", "test"]
    debug = 1 if env in debug_environments else 0
    secret_key = get_random_secret_key()

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


def main():
    repo = Repo.init(".")
    elements = repo.remotes.origin.url.split(".git")[0].split("/")
    username = elements[-2]
    project_default = elements[-1]
    repo_default = f"{username}/{project_default}"

    print_intro()
    project = get_project(project_default)
    repo = get_repo(repo_default)
    deployer = get_deployer()
    users = get_users_appname()

    dev_db = get_database("development")
    dev_db_user = get_database_user("development")
    dev_db_password = get_database_password("development")

    test_db = get_database("testing")
    test_db_user = get_database_user("testing")
    test_db_password = get_database_password("testing")

    prod_db = get_database("production")
    prod_db_user = get_database_user("production")
    prod_db_password = get_database_password("production")

    settings = f"./src/{project}/settings.py"
    create_django_project(project)
    create_users_app(users)
    create_users_model(users)
    exempt_long_lines(settings)
    change_settings(settings, users)
    change_cd_workflow(project, deployer)
    change_dockerfile(project)
    change_compose_prod(repo, deployer)
    change_pytest_ini(project)
    change_readme(project)
    make_env("dev", dev_db, dev_db_user, dev_db_password)
    make_env("test", test_db, test_db_user, test_db_password)
    make_env("prod", prod_db, prod_db_user, prod_db_password)


if __name__ == "__main__":
    main()
