import files
import messages
import processes
import prompts
import repo
from git import Repo


def main():
    repository = Repo.init(".")
    url = repository.remotes.origin.url
    default_username, github_project_name, default_repository = repo.get_repo(url)
    default_project_name = prompts.underscores_for_dashes(github_project_name)

    messages.print_intro()
    project = prompts.get_project(default_project_name)
    repository = prompts.get_repo(default_repository)
    deployer = prompts.get_deployer()
    users = prompts.get_users_appname()

    environments = {
        "dev": {
            "db": prompts.get_database("development"),
            "db_user": prompts.get_database_user("development"),
            "db_password": prompts.get_database_password("development"),
            "debug": 1,
        },
        "test": {
            "db": prompts.get_database("test"),
            "db_user": prompts.get_database_user("test"),
            "db_password": prompts.get_database_password("test"),
            "debug": 1,
        },
        "prod": {
            "db": prompts.get_database("production"),
            "db_user": prompts.get_database_user("production"),
            "db_password": prompts.get_database_password("production"),
            "debug": 0,
        },
    }

    settings_file = f"./src/{project}/settings.py"

    processes.create_django_project(project)
    processes.create_users_app(users)

    files.create_users_model_test(users)
    files.create_users_model(users)
    files.change_settings(settings_file, users)
    files.exempt_long_lines(settings_file)
    files.change_urls(project)
    files.change_cd_workflow(project, deployer)
    files.change_dockerfile(project)
    files.change_pytest_ini(project)
    files.change_readme(project)
    files.change_scripts(project)
    files.change_compose_prod(repository, deployer, "prod")

    for env in environments:
        files.make_env(
            env=env,
            db=environments[env]["db"],
            db_user=environments[env]["db_user"],
            db_password=environments[env]["db_password"],
            debug=environments[env]["debug"],
        )


if __name__ == "__main__":
    main()
