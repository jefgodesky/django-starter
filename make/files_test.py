from unittest.mock import mock_open

import files
import pytest


@pytest.fixture
def mock_file(monkeypatch):
    mock = mock_open()
    monkeypatch.setattr("builtins.open", mock)
    return mock


def test_exempt_long_lines_lt(mock_file):
    content = "A" * 87 + "\n"
    mock_file().readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file().writelines.call_args[0][0]
    assert actual == [content]


def test_exempt_long_lines_eq(mock_file):
    content = "A" * 88 + "\n"
    mock_file().readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file().writelines.call_args[0][0]
    assert actual == [content]


def test_exempt_long_lines_gt(mock_file):
    content = "A" * 89 + "\n"
    mock_file().readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file().writelines.call_args[0][0]
    assert actual == ["A" * 89 + "  # noqa: E501\n"]


def test_create_users_model_tests_content(mock_file):
    files.create_users_model_tests("users")
    actual = mock_file().write.call_args[0][0]
    assert "from .models import UserAccount" in actual


def test_create_users_model_tests_filename(mock_file):
    files.create_users_model_tests("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/models_test.py"
    assert args[1] == "w"


def test_create_users_model_content(mock_file):
    files.create_users_model("users")
    actual = mock_file().write.call_args[0][0]
    assert "class UserAccount(AbstractBaseUser):" in actual


def test_create_users_model_filename(mock_file):
    files.create_users_model("users")
    args = mock_file.call_args[0]
    assert args[0] == "./src/users/models.py"
    assert args[1] == "w"
