from unittest.mock import mock_open

import files
import pytest


@pytest.fixture
def mock_file(monkeypatch):
    mock = mock_open()
    monkeypatch.setattr("builtins.open", mock)
    return mock()


def test_exempt_long_lines_lt(mock_file):
    content = "A" * 87 + "\n"
    mock_file.readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file.writelines.call_args[0][0]
    assert actual == [content]


def test_exempt_long_lines_eq(mock_file):
    content = "A" * 88 + "\n"
    mock_file.readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file.writelines.call_args[0][0]
    assert actual == [content]


def test_exempt_long_lines_gt(mock_file):
    content = "A" * 89 + "\n"
    mock_file.readlines.return_value = [content]
    files.exempt_long_lines("test.txt")
    actual = mock_file.writelines.call_args[0][0]
    assert actual == ["A" * 89 + "  # noqa: E501\n"]
