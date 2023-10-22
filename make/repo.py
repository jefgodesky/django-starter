def get_repo(url):
    elements = url.split(".git")[0].split("/")
    username = elements[-2]
    project_name = elements[-1]
    repository = f"{username}/{project_name}"
    return username, project_name, repository
