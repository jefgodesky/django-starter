import subprocess


def create_django_project(project: str):
    subprocess.run(["django-admin", "startproject", project, "."], cwd="src")


def create_users_app(users: str):
    subprocess.run(["python", "manage.py", "startapp", users], cwd="src")


def create_templates_dir(project: str):
    subprocess.run(["mkdir", "-p", f"{project}/templates/registration"], cwd="src")
