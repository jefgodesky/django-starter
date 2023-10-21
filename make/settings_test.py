import settings

test_example = """INSTALLED_APPS = [
    \"previously_installed\",
]"""


def test_add_installed_apps_keeps_previous():
    actual = settings.add_installed_apps(test_example, "users")
    assert '"previously_installed",' in actual


def test_add_installed_apps_adds_rest_framework():
    actual = settings.add_installed_apps(test_example, "users")
    assert '"rest_framework",' in actual


def test_add_installed_apps_adds_users():
    actual = settings.add_installed_apps(test_example, "users")
    assert '"users",' in actual
