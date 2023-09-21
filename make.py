import os
import re
import subprocess
from inspect import cleandoc

from django.core.management.utils import get_random_secret_key


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


def get_project():
    msg = "What would you like to call your project?"
    prompt_text = "Project name: "
    return prompt(msg, prompt_text)


def get_droplet():
    msg = """What’s the name of your DigitalOcean droplet (used to locate
      your Docker images in the DigitalOcean Container Registry; e.g.,
      registry.digitalocean.com/DROPLET)?"""
    prompt_text = "Droplet name: "
    return prompt(cleandoc(msg), prompt_text)


def get_repo():
    msg = """What’s the name of your repository (also used to locate your
      Docker images in the DigitalOcean Container Registry, e.g.,
      registry.digitalocean.com/DROPLET/REPO)?"""
    prompt_text = "Repository name: "
    return prompt(cleandoc(msg), prompt_text)


def get_deployer():
    msg = """You’ll want to create a non-root user on your DigitalOcean droplet
      who has all the permissions it needs to deploy your Docker containers.
      This should be an account separate from any human user, one dedicated entirely
      to automated, continuous delivery. What is this user’s user name?"""
    prompt_text = "Deployment username: "
    return prompt(cleandoc(msg), prompt_text)


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
    subprocess.run(["django-admin", "startproject", project, "src"])


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


def add_installed_apps(settings: str):
    apps_to_add = ['"rest_framework"']
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


def change_settings(filename: str):
    with open(filename) as file:
        settings = file.read()

    settings = add_installed_apps(settings)
    settings = change_database_settings(settings)
    replacements = [
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


def change_cd_workflow(filename: str, droplet: str, repo: str, droplet_user: str):
    with open(filename) as file:
        workflow = file.read()

    replacements = [
        ('"{{ droplet }}"', droplet),
        ('"{{ repo }}"', repo),
        ('"{{ droplet_user }}"', droplet_user),
    ]

    for pattern, replacement in replacements:
        workflow = workflow.replace(pattern, replacement)

    with open(filename, "w") as file:
        file.write(workflow)


def change_dockerfile(project: str):
    with open("docker/Dockerfile") as file:
        dockerfile = file.read()

    dockerfile = dockerfile.replace(
        'ARG SITENAME="django_starter"', f'ARG SITENAME="{project}"'
    )

    with open("docker/Dockerfile", "w") as file:
        file.write(dockerfile)


def change_docker_compose(db: str, user: str, password: str):
    with open("docker/docker-compose.yml") as file:
        yml = file.read()

    replacements = [
        ("POSTGRES_DB: myproject_db", f"POSTGRES_DB: {db}"),
        ("POSTGRES_USER: django_db_user", f"POSTGRES_USER: {user}"),
        ("POSTGRES_PASSWORD: password", f"POSTGRES_PASSWORD: {password}"),
    ]

    for pattern, replacement in replacements:
        yml = yml.replace(pattern, replacement)

    with open("docker/docker-compose.yml", "w") as file:
        file.write(yml)


def make_env(env: str, db: str, db_user: str, db_password: str):
    with open("docker/.env.example") as example:
        settings = example.read()

    debug = 1 if env == "prod" else 0
    secret_key = get_random_secret_key()

    replacements = [
        ("DEBUG=1", f"DEBUG={debug}"),
        ("SECRET_KEY=your_secret_key_here", f"SECRET_KEY={secret_key}"),
        ("SQL_DATABASE=myproject_db", f"SQL_DATABASE={db}"),
        ("SQL_USER=django_db_user", f"SQL_USER={db_user}"),
        ("SQL_PASSWORD=password", f"SQL_PASSWORD={db_password}"),
    ]

    for pattern, replacement in replacements:
        settings = settings.replace(pattern, replacement)

    with open(f"docker/.env.{env}", "w") as file:
        file.write(settings)


def print_conclusion(project: str):
    os.system("clear")
    title = f"{project} is ready!"
    intro = """If you want to use a custom user model, now’s the time to write your
      first, most basic test for that. If not, you can run:

      cd src
      poetry shell
      python manage.py makemigrations
      python manage.py migrate
      python manage.py runserver

      ...to see your site up and running.

      For other next steps, visit:

      https://github.com/jefgodesky/django-starter"""
    print_bold(title)
    print(cleandoc(intro))


def main():
    print_intro()
    project = get_project()
    droplet = get_droplet()
    repo = get_repo()
    deployer = get_deployer()

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
    exempt_long_lines(settings)
    change_settings(settings)
    change_cd_workflow("./.github/workflows/cd.yml", droplet, repo, deployer)
    change_dockerfile(project)
    change_docker_compose(dev_db, dev_db_user, dev_db_password)
    make_env("dev", dev_db, dev_db_user, dev_db_password)
    make_env("test", test_db, test_db_user, test_db_password)
    make_env("prod", prod_db, prod_db_user, prod_db_password)
    print_conclusion(project)


if __name__ == "__main__":
    main()
