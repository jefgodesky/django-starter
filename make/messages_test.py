import messages
import pytest


def test_print_bold(capsys):
    messages.print_bold("Hello, world!")
    captured = capsys.readouterr()
    expected = "\033[1mHello, world!\033[0m\n"
    assert captured.out == expected


def test_print_intro_bold_title(capsys):
    messages.print_intro()
    captured = capsys.readouterr()
    expected = "\033[1mLet’s start a new Django project!\033[0m\n"
    assert expected in captured.out


def test_print_intro_text(capsys):
    messages.print_intro()
    captured = capsys.readouterr()
    expected = "This script will help you get set up"
    assert expected in captured.out


@pytest.fixture
def prompt_setup(monkeypatch, capsys):
    test_input = "Test"
    monkeypatch.setattr("builtins.input", lambda _: test_input)
    test_msg = "Test message."
    test_prompt = "Test: "
    result = messages.prompt(test_msg, test_prompt)
    captured = capsys.readouterr().out
    return captured, result, test_msg, test_prompt, test_input


def test_prompt_show_message(prompt_setup):
    captured, _, test_msg, _, _ = prompt_setup
    assert test_msg in captured


def test_prompt_gets_input(prompt_setup):
    _, result, _, _, test_input = prompt_setup
    assert result == test_input
