import repo


def test_get_repo():
    url = "https://github.com/jefgodesky/django-starter.git"
    username, project_name, repository = repo.get_repo(url)
    assert username == "jefgodesky"
    assert project_name == "django-starter"
    assert repository == "jefgodesky/django-starter"
