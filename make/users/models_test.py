import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def create_test_user():
    username = "tester"
    email = "tester@testing.com"
    password = "testpassword123"
    user = get_user_model().objects.create_user(
        username=username, email=email, password=password
    )
    return user


@pytest.mark.django_db
def test_user_account_username(create_test_user):
    assert create_test_user.username == "tester"


@pytest.mark.django_db
def test_user_account_email(create_test_user):
    assert create_test_user.email == "tester@testing.com"


@pytest.mark.django_db
def test_user_account_str(create_test_user):
    assert str(create_test_user.username) == "tester"
