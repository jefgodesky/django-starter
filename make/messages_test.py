import messages


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
