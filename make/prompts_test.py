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
