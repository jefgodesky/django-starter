import os
from unittest.mock import MagicMock, mock_open

import files
import pytest


@pytest.fixture
def mock_file(monkeypatch):
    mock = mock_open()
    monkeypatch.setattr("builtins.open", mock)
    return mock


def test_replace_in_file_open_file(mock_file):
    files.replace_in_file("test.txt", [(r"in", "out")])
    args = mock_file.call_args_list[0][0]
    assert args[0] == "test.txt"
    assert len(args) == 1


def test_replace_in_file_text(mock_file):
    mock_file().read.return_value = "in"
    files.replace_in_file("test.txt", [(r"in", "out")])
    actual = mock_file().write.call_args[0][0]
    assert actual == "out"


def test_replace_in_file_regex(mock_file):
    mock_file().read.return_value = "in/something\n"
    files.replace_in_file("test.txt", [(r"in\/(.*?)\n", "out")])
    actual = mock_file().write.call_args[0][0]
    assert actual == "out"


def test_replace_in_file_write_file(mock_file):
    files.replace_in_file("test.txt", [(r"in", "out")])
    args = mock_file.call_args_list[1][0]
    assert args[0] == "test.txt"
    assert args[1] == "w"
    assert len(args) == 2


def test_replace_in_file_write_file_dest(mock_file):
    files.replace_in_file("src.txt", [(r"in", "out")], "dest.txt")
    args = mock_file.call_args_list[1][0]
    assert args[0] == "dest.txt"
    assert args[1] == "w"
    assert len(args) == 2


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


def test_change_cd_workflow_makedirs(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    makedirs_mock = MagicMock()
    monkeypatch.setattr(os, "makedirs", makedirs_mock)
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.change_cd_workflow("myproject", "user")
    makedirs_mock.assert_called_once()


def test_change_cd_workflow_skip_makedirs(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    makedirs_mock = MagicMock()
    monkeypatch.setattr(os, "makedirs", makedirs_mock)
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.change_cd_workflow("myproject", "user")
    makedirs_mock.assert_not_called()


def test_change_cd_workflow_args(mock_file, monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    monkeypatch.setattr(os, "makedirs", lambda _: None)
    replace_in_file_mock = MagicMock()
    monkeypatch.setattr(files, "replace_in_file", replace_in_file_mock)
    files.change_cd_workflow("myproject", "user")
    replace_in_file_mock.assert_called_once_with(
        "cd.yml",
        [("PROJECT", "myproject"), ("DEPLOYER_USERNAME", "user")],
        dest="./.github/workflows/cd.yml",
    )
