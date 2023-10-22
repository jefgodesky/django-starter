import prompts
import pytest


def mock_empty_prompt(msg, prompt_text):
    print("\n" + msg)
    return ""


@pytest.fixture
def prompt_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    test_msg = "Test message."
    test_prompt = "Test: "
    result = prompts.prompt(test_msg, test_prompt)
    captured = capsys.readouterr().out
    return captured, result, test_msg, test_input


def test_prompt_show_message(prompt_setup):
    captured, _, test_msg, _ = prompt_setup
    assert test_msg in captured


def test_prompt_gets_input(prompt_setup):
    _, result, _, test_input = prompt_setup
    assert result == test_input


@pytest.fixture
def prompt_password_setup(monkeypatch, capfd):
    test_msg = "Test message."
    test_password = "password"
    monkeypatch.setattr(prompts, "getpass", lambda _: test_password)
    result = prompts.prompt_password(test_msg, "Password: ")
    out, err = capfd.readouterr()
    return out, err, result, test_msg, test_password


def test_prompt_password_show_message(prompt_password_setup):
    out, _, _, test_msg, _ = prompt_password_setup
    assert test_msg in out


def test_prompt_password_password_not_shown(prompt_password_setup):
    _, err, _, _, test_password = prompt_password_setup
    assert test_password not in err


def test_prompt_password_password_returned(prompt_password_setup):
    _, _, result, _, test_password = prompt_password_setup
    assert test_password == result


@pytest.fixture
def get_project_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_project("")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_project_show_message(get_project_setup):
    captured, _, _ = get_project_setup
    assert "What would you like to call your project?" in captured


def test_get_project_gets_input(get_project_setup):
    _, result, test_input = get_project_setup
    assert result == test_input


def test_get_project_gets_default(monkeypatch):
    default_value = "default"
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_project(default_value)
    assert result == default_value


@pytest.fixture
def get_repo_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_repo("")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_repo_show_message(get_repo_setup):
    captured, _, _ = get_repo_setup
    assert "What is the name of your GitHub repository?" in captured


def test_get_repo_gets_input(get_repo_setup):
    _, result, test_input = get_repo_setup
    assert result == test_input


def test_get_repo_gets_default(monkeypatch):
    default_value = "default"
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_repo(default_value)
    assert result == default_value


@pytest.fixture
def get_deployer_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_deployer()
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_deployer_show_message(get_deployer_setup):
    captured, _, _ = get_deployer_setup
    assert "You’ll want to create a non-root user" in captured


def test_get_deployer_gets_input(get_deployer_setup):
    _, result, test_input = get_deployer_setup
    assert result == test_input


@pytest.fixture
def get_users_appname_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_users_appname()
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_users_appname_show_message(get_users_appname_setup):
    captured, _, _ = get_users_appname_setup
    expected = "What would you like to call the app that handles your users?"
    assert expected in captured


def test_get_users_appname_gets_input(get_users_appname_setup):
    _, result, test_input = get_users_appname_setup
    assert result == test_input


def test_get_users_appname_gets_default(monkeypatch):
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_users_appname()
    assert result == "users"


@pytest.fixture
def get_database_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_database("test")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_database_show_message(get_database_setup):
    captured, _, _ = get_database_setup
    assert "in your test environment?" in captured


def test_get_database_gets_input(get_database_setup):
    _, result, test_input = get_database_setup
    assert result == test_input


@pytest.fixture
def get_database_user_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_database_user("test")
    captured = capsys.readouterr().out
    return captured, result, test_input


def test_get_database_user_show_message(get_database_user_setup):
    captured, _, _ = get_database_user_setup
    assert "for your test environment database?" in captured


def test_get_database_user_gets_input(get_database_user_setup):
    _, result, test_input = get_database_user_setup
    assert result == test_input


@pytest.fixture
def get_database_password_setup(monkeypatch, capfd):
    test_password = "password"
    monkeypatch.setattr(prompts, "getpass", lambda _: test_password)
    result = prompts.get_database_password("test")
    out, err = capfd.readouterr()
    return out, err, result, test_password


def test_get_database_password_show_message(get_database_password_setup):
    out, _, _, _ = get_database_password_setup
    assert "for your test environment database?" in out


def test_get_database_password_password_not_shown(get_database_password_setup):
    _, err, _, test_password = get_database_password_setup
    assert test_password not in err


def test_get_database_password_gets_input(get_database_password_setup):
    _, _, result, test_input = get_database_password_setup
    assert result == test_input


@pytest.fixture
def get_debug_environments_setup(monkeypatch, capsys):
    test_input = "devx, testx"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_debug_environments()
    captured = capsys.readouterr().out
    return captured, result


def test_get_debug_environments_show_message(get_debug_environments_setup):
    captured, _ = get_debug_environments_setup
    assert "Provide a comma-separated list of environments" in captured


def test_get_debug_environments_gets_input(get_debug_environments_setup):
    _, result = get_debug_environments_setup
    assert result == ["devx", "testx"]


def test_get_debug_environments_gets_default(monkeypatch):
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_debug_environments()
    assert result == ["dev", "test"]


@pytest.fixture
def get_prod_environments_setup(monkeypatch, capsys):
    test_input = "blue, green"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    result = prompts.get_prod_environments()
    captured = capsys.readouterr().out
    return captured, result


def test_get_prod_environments_show_message(get_prod_environments_setup):
    captured, _ = get_prod_environments_setup
    assert "Provide a comma-separated list of environments" in captured


def test_get_prod_environments_gets_input(get_prod_environments_setup):
    _, result = get_prod_environments_setup
    assert result == ["blue", "green"]


def test_get_prod_environments_gets_default(monkeypatch):
    monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
    result = prompts.get_prod_environments()
    assert result == ["prod"]


def test_get_starter_env_debug():
    env = "test"
    actual = prompts.get_starter_env(env, debug=True)
    assert actual["env"] == env
    assert actual["db"] is None
    assert actual["db_user"] is None
    assert actual["db_password"] is None
    assert actual["debug"] is True


def test_get_starter_env_prod():
    env = "prod"
    actual = prompts.get_starter_env(env)
    assert actual["env"] == env
    assert actual["db"] is None
    assert actual["db_user"] is None
    assert actual["db_password"] is None
    assert actual["debug"] is False


@pytest.fixture
def get_environment_settings_setup(monkeypatch, capfd):
    test_input = "test"
    test_password = "password"
    monkeypatch.setattr(prompts, "getpass", lambda _: test_password)
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    dictionary = prompts.get_starter_env(test_input, debug=True)
    result = prompts.get_environment_settings(dictionary)
    out, err = capfd.readouterr()
    return result, test_input, test_password


def get_environment_settings_dictionary(get_environment_settings_setup):
    result, test_input, test_password = get_environment_settings_setup
    assert result["env"] == test_input
    assert result["db"] == test_input
    assert result["db_user"] == test_input
    assert result["db_password"] == test_password
    assert result["debug"] is True


def test_get_env_dict():
    debug_env = ["dev", "test"]
    prod_env = ["green", "blue"]
    actual = prompts.get_env_dict(debug=debug_env, prod=prod_env)

    assert actual["dev"]["env"] == "dev"
    assert actual["dev"]["db"] is None
    assert actual["dev"]["db_user"] is None
    assert actual["dev"]["db_password"] is None
    assert actual["dev"]["debug"] is True

    assert actual["test"]["env"] == "test"
    assert actual["test"]["db"] is None
    assert actual["test"]["db_user"] is None
    assert actual["test"]["db_password"] is None
    assert actual["test"]["debug"] is True

    assert actual["green"]["env"] == "green"
    assert actual["green"]["db"] is None
    assert actual["green"]["db_user"] is None
    assert actual["green"]["db_password"] is None
    assert actual["green"]["debug"] is False

    assert actual["blue"]["env"] == "blue"
    assert actual["blue"]["db"] is None
    assert actual["blue"]["db_user"] is None
    assert actual["blue"]["db_password"] is None
    assert actual["blue"]["debug"] is False
