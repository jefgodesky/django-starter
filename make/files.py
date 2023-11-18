import os
import re

import black
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

    replace_in_file("src/.pytest.ini", replacements, dest="src/pytest.ini")


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


def change_urls(project: str, api_only: bool = False):
    filename = f"./src/{project}/urls.py"

    with open(filename) as file:
        contents = file.read()

    imports = []
    found_imports = re.findall(r"^from (.*?) import (.*?)$", contents, re.MULTILINE)
    for import_statement in found_imports:
        source = import_statement[0]
        item = import_statement[1]
        if source == "django.urls":
            item = "include, " + item
        imports.append(f"from {source} import {item}")

    if not api_only:
        imports.append("from django.views.generic.base import TemplateView")

    imports = sorted(imports + ["from django.conf import settings"]) + [
        "from rest_framework import permissions",
        "from drf_yasg.views import get_schema_view",
        "from drf_yasg import openapi",
    ]

    variables = [
        f'app_name = "{project}"',
        "api = settings.API_BASE",
    ]

    schema_view = """schema_view = get_schema_view(
    openapi.Info(
        title="PROJECT API",
        default_version="v1",
        description="API for PROJECT",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)"""
    schema_view = schema_view.replace("PROJECT", project)

    regex = r"urlpatterns = \[(.*?)]"
    search = re.search(regex, contents, flags=re.DOTALL | re.MULTILINE)
    urlpatterns_str = "" if search is None else search.group(1).strip()
    found_urlpatterns = urlpatterns_str.split(os.linesep)
    urlpatterns = found_urlpatterns

    if not api_only:
        home = 'TemplateView.as_view(template_name="home.html")'
        urlpatterns.append(f'path("", {home}, name="home"),')
        urlpatterns.append('path("", include("users.urls")),')
        urlpatterns.append('path("", include("django.contrib.auth.urls")),')

    urlpatterns = urlpatterns + [
        'path(f"{api}/doc<format>", schema_view.without_ui(cache_timeout=0), name="schema-json"),',  # noqa: E501
        'path(f"{api}/doc/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),',  # noqa: E501
        'path(f"{api}/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),',  # noqa: E501
    ]

    urlpatterns = [f"    {pattern}" for pattern in urlpatterns]

    section_break = os.linesep * 2
    import_section = os.linesep.join(imports)
    var_section = os.linesep.join(variables)
    urlpatterns_section_inner = os.linesep.join(urlpatterns)
    urlpatterns_section = f"urlpatterns = [\n{urlpatterns_section_inner}\n]"
    urlpatterns_section = black.format_str(urlpatterns_section, mode=black.FileMode())
    sections = [import_section, var_section, schema_view, urlpatterns_section]

    with open(filename, "w") as file:
        file.write(section_break.join(sections) + os.linesep)


def change_settings(filename: str, users: str, api_only: bool = False):
    with open(filename) as file:
        contents = file.read()

    contents = settings.add_installed_apps(contents, users)
    contents = settings.change_database_settings(contents)
    contents = settings.set_project_template_dir(contents)
    contents = settings.add_new_settings(contents, users, api_only=api_only)
    contents = settings.add_import_os(contents)
    contents = settings.set_secret_key(contents)
    contents = settings.set_debug(contents)
    contents = settings.set_allowed_hosts(contents)
    contents = settings.add_prod_rest_framework_renderer(contents)

    with open(filename, "w") as file:
        file.write(contents)


def copy_files(project: str, users: str, api_only: bool = False):
    files = {
        "make/.conftest.py": "./src/conftest.py",
        "make/test.sh": "./src/test.sh",
        "make/templates/400.html": f"./src/{project}/templates/400.html",
        "make/templates/403.html": f"./src/{project}/templates/403.html",
        "make/templates/404.html": f"./src/{project}/templates/404.html",
        "make/templates/500.html": f"./src/{project}/templates/500.html",
        "make/users/admin.py": f"./src/{users}/admin.py",
        "make/users/forms.py": f"./src/{users}/forms.py",
        "make/users/models.py": f"./src/{users}/models.py",
        "make/users/models.test.py": f"./src/{users}/models_test.py",
        "make/users/serializers.py": f"./src/{users}/serializers.py",
        "make/users/serializers.test.py": f"./src/{users}/serializers_test.py",
        "make/users/views.py": f"./src/{users}/views.py",
        "make/users/views.test.py": f"./src/{users}/views_test.py",
        "make/users/templates/login.html": f"./src/{users}/templates/login.html",
        "make/users/templates/register.html": f"./src/{users}/templates/register.html",
    }

    urls = "make/users/urls.api-only.py" if api_only else "make/users/urls.py"
    files[urls] = f"./src/{users}/urls.py"

    for file in files:
        replace_in_file(file, [], dest=files[file])


def add_provider_env(providers, env="prod"):
    filename = f"docker/.env.{env}"

    with open(filename) as file:
        contents = file.read()

    for provider in providers:
        prefix = "SNAPCHAT" if provider == "snap" else provider.upper()
        contents += f"\n{prefix}_CLIENT_ID=your_{prefix}_secret_here{os.linesep}"
        contents += f"\n{prefix}_SECRET=your_{prefix}_secret_here{os.linesep}"
        contents += f"\n{prefix}_KEY=your_{prefix}_key_here{os.linesep}"

        if provider == "apple":
            contents += "APPLE_CERTIFICATE_KEY=your_cert_here" + os.linesep

        if provider == "auth0":
            contents += "AUTH0_URL=your_url_here" + os.linesep

        if provider == "reddit":
            contents += "REDDIT_USERNAME=your_reddit_username_here" + os.linesep

    with open(filename, "w") as file:
        file.write(contents)


def make_next(providers: list):
    fragments = []

    with open("./next/1.md") as file:
        fragments.append(file.read())

    for provider in providers:
        with open(f"./next/{provider}.md") as file:
            fragments.append(file.read())

    with open("./next/2.md") as file:
        fragments.append(file.read())

    with open("./next.md", "w") as file:
        file.write(os.linesep.join(fragments))
