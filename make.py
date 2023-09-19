import os
import re
import subprocess
from inspect import cleandoc


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


def get_user():
    msg = """You’ll want to create a non-root user on your DigitalOcean droplet
      who has all the permissions it needs to deploy your Docker containers.
      This should be an account separate from any human user, one dedicated entirely
      to automated, continuous delivery. What is this user’s user name?"""
    prompt_text = "Username: "
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

      ...to see your site up and running."""
    print_bold(title)
    print(cleandoc(intro))


def main():
    print_intro()
    project = get_project()
    droplet = get_droplet()
    repo = get_repo()
    user = get_user()
    settings = f"./src/{project}/settings.py"
    create_django_project(project)
    exempt_long_lines(settings)
    change_settings(settings)
    change_cd_workflow("./.github/workflows/cd.yml", droplet, repo, user)
    print_conclusion(project)


if __name__ == "__main__":
    main()
