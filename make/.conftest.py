# These are some shared fixtures used in the users app unit tests, which you
# will likely find useful in your own tests, particularly when testing
# permissions and access rights.

import json

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from rest_framework.test import APIClient
from users.models import UserAccount

password = "testpass123"


def get_or_create_user(username: str, is_staff=False):
    email = f"{username}@testing.com"
    user, created = UserAccount.objects.get_or_create(
        username=username, email=email, defaults={"is_staff": is_staff}
    )
    if created:
        user.set_password(password)
        user.save()
    return user


def auth_client(client, user):
    endpoint = f"/{settings.API_BASE}session/"
    data = json.dumps({"username": user.username, "password": password})
    response = client.post(endpoint, data, content_type="application/json")
    client.credentials(HTTP_AUTHORIZATION="Token " + response.data["key"])
    return client


@pytest.mark.django_db
def verify_user(user):
    email_address, created = EmailAddress.objects.get_or_create(
        user=user, email=user.email
    )
    email_address.verified = True
    email_address.primary = True
    email_address.save()
    return user


@pytest.fixture
def anon():
    return AnonymousUser()


@pytest.fixture
def user():
    return get_or_create_user("user")


@pytest.fixture
def other():
    return get_or_create_user("other")


@pytest.fixture
def staff():
    return get_or_create_user("staff", is_staff=True)


@pytest.fixture
def verified_user(user):
    return verify_user(user)


@pytest.fixture
def verified_other(other):
    return verify_user(other)


@pytest.fixture
def verified_staff(staff):
    return verify_user(staff)


@pytest.fixture
def anon_client():
    client = APIClient()
    return client, AnonymousUser()


@pytest.fixture
def user_client(anon_client, verified_user):
    client = auth_client(APIClient(), verified_user)
    yield client, verified_user
    client.logout()


@pytest.fixture
def other_client(anon_client, verified_other):
    client = auth_client(APIClient(), verified_other)
    yield client, verified_other
    client.logout()


@pytest.fixture
def staff_client(anon_client, verified_staff):
    client = auth_client(APIClient(), verified_staff)
    yield client, verified_staff
    client.logout()


@pytest.fixture
@pytest.mark.django_db
def anon_browser():
    return Client(), AnonymousUser()


@pytest.fixture
@pytest.mark.django_db
def user_browser(verified_user):
    client = Client()
    client.login(username=verified_user.username, password="testpass123")
    return client, verified_user


@pytest.fixture
@pytest.mark.django_db
def other_browser(verified_other):
    client = Client()
    client.login(username=verified_other.username, password="testpass123")
    return client, verified_other


@pytest.fixture
@pytest.mark.django_db
def staff_browser(verified_staff):
    client = Client()
    client.login(username=verified_staff.username, password="testpass123")
    return client, verified_staff


@pytest.fixture
def get_user(request, anon, verified_user, verified_other, verified_staff):
    match request.param:
        case "anon":
            return anon
        case "user":
            return verified_user
        case "other":
            return verified_other
        case "staff":
            return verified_staff


@pytest.fixture
def get_client(request, anon_client, user_client, other_client, staff_client):
    match request.param:
        case "anon":
            return anon_client
        case "user":
            return user_client
        case "other":
            return other_client
        case "staff":
            return staff_client
