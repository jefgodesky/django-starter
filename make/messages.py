from inspect import cleandoc


def print_bold(msg: str):
    print("\033[1m" + msg + "\033[0m")


def print_intro():
    title = "Let’s start a new Django project!"
    intro = """This script will help you get set up for a new Django project. It’s quite
      opinionated, though. If you’re interested in running a Dockerized, API-first
      Django site using test-driven development (TDD) and continuous delivery (CD)
      to a Digital Ocean droplet, then this script will give you a great starting
      point. If you’re looking for something else, then I’m afraid this script won’t
      be of much help to you. Godspeed on your journey, friend. But if that is what
      you’re looking for, well, let’s get started!"""
    print_bold(title)
    print(cleandoc(intro))


def prompt(msg: str, prompt_text: str):
    print("\n" + msg)
    return input(prompt_text)
