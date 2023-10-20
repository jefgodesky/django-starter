import messages


def test_print_bold(capsys):
    messages.print_bold("Hello, world!")
    captured = capsys.readouterr()
    expected = "\033[1mHello, world!\033[0m\n"
    assert captured.out == expected
