import prompts
import pytest


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

    def mock_prompt(msg, prompt_text):
        print("\n" + msg)
        return ""

    monkeypatch.setattr(prompts, "prompt", mock_prompt)
    result = prompts.get_project(default_value)
    assert result == default_value
