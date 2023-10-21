import subprocess


def create_django_project(project: str):
    subprocess.run(["django-admin", "startproject", project, "."], cwd="src")
