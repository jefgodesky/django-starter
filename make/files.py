def exempt_long_lines(filename: str):
    with open(filename) as file:
        lines = file.readlines()

    modified_lines = [
        line.rstrip() + "  # noqa: E501\n"
        if len(line.rstrip()) > 88
        else line.rstrip() + "\n"
        for line in lines
    ]

    with open(filename, "w") as file:
        file.writelines(modified_lines)


def create_users_model_tests(users: str):
    content = """import pytest
import datetime
from django.utils import timezone
from .models import UserAccount


@pytest.mark.django_db
def test_active_default():
    account = UserAccount()
    assert account.is_active is True


@pytest.mark.django_db
def test_created_default():
    before = timezone.now()
    account = UserAccount()
    after = timezone.now()
    assert isinstance(account.created, datetime.datetime)
    assert before <= account.created
    assert after >= account.created
"""

    with open(f"./src/{users}/models_test.py", "w") as file:
        file.write(content)
