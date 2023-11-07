import prompts
import pytest


def mock_empty_prompt(self, msg):
    print("\n" + msg)
    return ""


class TestPrompt:
    @pytest.fixture
    def setup(self, monkeypatch, capsys):
        test_input = "Test"
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        test_msg = "Test message."
        test_prompt = "Test: "
        result = prompts.prompt(test_msg, test_prompt)
        captured = capsys.readouterr().out
        return captured, result, test_msg, test_input

    def test_prompt_show_message(self, setup):
        captured, _, test_msg, _ = setup
        assert test_msg in captured

    def test_prompt_gets_input(self, setup):
        _, result, _, test_input = setup
        assert result == test_input

    def test_prompt_requires_input(self, monkeypatch):
        input_generator = iter(["", "test"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
        result = prompts.prompt("Message", "Prompt: ", required=True)
        assert result == "test"

    def test_prompt_requires_option(self, monkeypatch):
        input_generator = iter(["x", "y"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
        result = prompts.prompt("Message", "Prompt: ", options={"y": True, "n": False})
        assert result is True


class TestPromptPassword:
    @pytest.fixture
    def setup(self, monkeypatch, capfd):
        test_msg = "Test message."
        test_password = "password"
        monkeypatch.setattr(prompts, "getpass", lambda _: test_password)
        result = prompts.prompt_password(test_msg, "Password: ")
        out, err = capfd.readouterr()
        return out, err, result, test_msg, test_password

    def test_show_message(self, setup):
        out, _, _, test_msg, _ = setup
        assert test_msg in out

    def test_password_not_shown(self, setup):
        _, err, _, _, test_password = setup
        assert test_password not in err

    def test_password_returned(self, setup):
        _, _, result, _, test_password = setup
        assert test_password == result


class TestGetProject:
    @pytest.fixture
    def setup(self, monkeypatch, capsys):
        test_input = "test"
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        result = prompts.get_project("")
        captured = capsys.readouterr().out
        return captured, result, test_input

    def test_show_message(self, setup):
        captured, _, _ = setup
        assert "What would you like to call your project?" in captured

    def test_gets_input(self, setup):
        _, result, test_input = setup
        assert result == test_input

    def test_gets_default(self, monkeypatch):
        default_value = "default"
        monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
        result = prompts.get_project(default_value)
        assert result == default_value

    def test_rejects_capitals(self, monkeypatch):
        input_generator = iter(["Test", "test"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
        result = prompts.get_project("myproject")
        assert result == "test"

    def test_rejects_dashes(self, monkeypatch):
        input_generator = iter(["test-example", "test_example"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
        result = prompts.get_project("myproject")
        assert result == "test_example"


class TestGetRepo:
    @pytest.fixture
    def setup(self, monkeypatch, capsys):
        test_input = "Test"
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        result = prompts.get_repo("")
        captured = capsys.readouterr().out
        return captured, result, test_input

    def test_show_message(self, setup):
        captured, _, _ = setup
        assert "What is the name of your GitHub repository?" in captured

    def test_gets_input(self, setup):
        _, result, test_input = setup
        assert result == test_input

    def test_gets_default(self, monkeypatch):
        default_value = "default"
        monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
        result = prompts.get_repo(default_value)
        assert result == default_value


class TestGetDeployer:
    @pytest.fixture
    def setup(self, monkeypatch, capsys):
        test_input = "Test"
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        result = prompts.get_deployer()
        captured = capsys.readouterr().out
        return captured, result, test_input

    def test_show_message(self, setup):
        captured, _, _ = setup
        assert "You’ll want to create a non-root user" in captured

    def test_gets_input(self, setup):
        _, result, test_input = setup
        assert result == test_input

    def test_required(self, monkeypatch):
        input_generator = iter(["", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
        result = prompts.get_deployer()
        assert result == "d"


class TestGetUsersAppName:
    @pytest.fixture
    def setup(self, monkeypatch, capsys):
        test_input = "Test"
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        result = prompts.get_users_appname()
        captured = capsys.readouterr().out
        return captured, result, test_input

    def test_show_message(self, setup):
        captured, _, _ = setup
        expected = "What would you like to call the app that handles your users?"
        assert expected in captured

    def test_gets_input(self, setup):
        _, result, test_input = setup
        assert result == test_input

    def test_gets_default(self, monkeypatch):
        monkeypatch.setattr(prompts, "prompt", mock_empty_prompt)
        result = prompts.get_users_appname()
        assert result == "users"


class TestGetDatabase:
    @pytest.fixture
    def setup(self, monkeypatch, capsys):
        test_input = "Test"
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        result = prompts.get_database("test")
        captured = capsys.readouterr().out
        return captured, result, test_input

    def test_show_message(self, setup):
        captured, _, _ = setup
        assert "in your test environment?" in captured

    def test_gets_input(self, setup):
        _, result, test_input = setup
        assert result == test_input

    def test_required(self, monkeypatch):
        input_generator = iter(["", "db"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
        result = prompts.get_database("test")
        assert result == "db"


class TestGetDatabaseUser:
    @pytest.fixture
    def setup(self, monkeypatch, capsys):
        test_input = "Test"
        monkeypatch.setattr("builtins.input", lambda _: test_input)
        result = prompts.get_database_user("test")
        captured = capsys.readouterr().out
        return captured, result, test_input

    def test_show_message(self, setup):
        captured, _, _ = setup
        assert "for your test environment database?" in captured

    def test_gets_input(self, setup):
        _, result, test_input = setup
        assert result == test_input

    def test_required(self, monkeypatch):
        input_generator = iter(["", "db_user"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_generator))
        result = prompts.get_database_user("test")
        assert result == "db_user"


class TestGetDatabasePassword:
    @pytest.fixture
    def setup(self, monkeypatch, capfd):
        test_password = "password"
        monkeypatch.setattr(prompts, "getpass", lambda _: test_password)
        result = prompts.get_database_password("test")
        out, err = capfd.readouterr()
        return out, err, result, test_password

    def test_show_message(self, setup):
        out, _, _, _ = setup
        assert "for your test environment database?" in out

    def test_password_not_shown(self, setup):
        _, err, _, test_password = setup
        assert test_password not in err

    def test_gets_input(self, setup):
        _, _, result, test_input = setup
        assert result == test_input


class TestGetAPIOnly:
    def test_shows_message(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "")
        prompts.get_api_only()
        captured = capsys.readouterr().out
        assert "Are you creating a standalone API?" in captured

    def test_defaults_false(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "x")
        result = prompts.get_api_only()
        assert result is False

    def test_takes_n(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "n")
        result = prompts.get_api_only()
        assert result is False

    def test_takes_no(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "No")
        result = prompts.get_api_only()
        assert result is False

    def test_takes_y(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "y")
        result = prompts.get_api_only()
        assert result is True

    def test_takes_yes(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "YeS")
        result = prompts.get_api_only()
        assert result is True


def test_underscores_for_dashes():
    actual = prompts.underscores_for_dashes("dashed-example-string")
    assert actual == "dashed_example_string"
