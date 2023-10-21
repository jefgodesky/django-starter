from getpass import getpass


def prompt(msg: str, prompt_text: str):
    print("\n" + msg)
    return input(prompt_text)


def prompt_password(msg: str, prompt_text: str):
    print("\n" + msg)
    return getpass(prompt_text)


def get_project(default_value: str):
    msg = "What would you like to call your project?"
    prompt_text = f"Project name ({default_value}): "
    return prompt(msg, prompt_text) or default_value


def get_repo(default_value: str):
    msg = "What is the name of your GitHub repository?"
    prompt_text = f"Repository ({default_value}): "
    return prompt(msg, prompt_text) or default_value
