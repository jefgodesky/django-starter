import files
import messages
import processes
import prompts
import repo
from git import Repo


def main():
    providers = []
    repository = Repo.init(".")
    url = repository.remotes.origin.url
    default_username, github_project_name, default_repository = repo.get_repo(url)
    default_project_name = prompts.underscores_for_dashes(github_project_name)

    messages.print_intro()
    project = prompts.get_project(default_project_name)
    repository = prompts.get_repo(default_repository)
    deployer = prompts.get_deployer()
    users = prompts.get_users_appname()
    api_only = prompts.get_api_only()
    if not api_only:
        social_auth = prompts.get_social_auth()
        if social_auth:
            providers = prompts.get_social_auth_providers()

    environments = {
        "dev": {"debug": 1},
        "test": {"debug": 1},
        "prod": {"debug": 0},
    }

    settings_file = f"./src/{project}/settings.py"

    processes.create_django_project(project)
    processes.create_users_app(users)

    files.copy_files(project, users)
    files.change_settings(settings_file, users, providers, api_only=api_only)
    files.exempt_long_lines(settings_file)
    files.change_urls(project)
    files.change_cd_workflow(project, deployer)
    files.change_dockerfile(project)
    files.change_pytest_ini(project)
    files.change_readme(project)
    files.change_scripts(project)
    files.change_compose_prod(repository, deployer, "prod")
    files.make_next(providers)

    for env in environments:
        files.make_env(
            env=env,
            debug=environments[env]["debug"],
        )
        files.add_provider_env(providers, env)


if __name__ == "__main__":
    main()
