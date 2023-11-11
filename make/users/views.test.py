import re

import pytest
from allauth.account.models import EmailAddress, EmailConfirmation
from django.conf import settings
from django.core import mail
from django.utils import timezone


def test_register_view(anon_client):
    client, _ = anon_client
    response = client.get("/register/")
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_client, expected",
    [("anon", 401), ("other", 403), ("user", 200), ("staff", 200)],
    indirect=["get_client"],
)
def test_user_detail(get_client, verified_user, expected):
    client, _ = get_client
    response = client.get(f"/{settings.API_BASE}users/{verified_user.id}/")
    assert response.status_code == expected
    if expected == 200:
        assert response.data["id"] == verified_user.id
        assert response.data["username"] == verified_user.username
        assert response.data["is_active"] == verified_user.is_active
        assert response.data["is_staff"] == verified_user.is_staff


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_client, expected",
    [("anon", 401), ("other", 403), ("user", 200), ("staff", 200)],
    indirect=["get_client"],
)
def test_user_delete(get_client, verified_user, expected):
    client, _ = get_client
    response = client.delete(f"/{settings.API_BASE}users/{verified_user.id}/")
    assert response.status_code == expected
    if expected == 200:
        assert response.data["id"] == verified_user.id
        assert response.data["username"] == verified_user.username
        assert response.data["is_active"] is False
        assert response.data["is_staff"] == verified_user.is_staff


@pytest.mark.django_db
def test_user_api_create(anon_client):
    client, _ = anon_client
    username = "testuser"
    password = "testpass123"
    response = client.post(
        f"/{settings.API_BASE}users/",
        {
            "username": username,
            "email": f"{username}@testing.com",
            "password1": password,
            "password2": password,
        },
    )
    assert response.status_code == 201
    assert response.data["username"] == username
    assert response.data["is_active"] is True
    assert response.data["is_staff"] is False


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password, expected",
    [("nope", "testpass123", 400), ("user", "nope", 400), ("user", "testpass123", 200)],
)
def test_session_post(anon_client, verified_user, username, password, expected):
    client, _ = anon_client
    response = client.post(
        f"/{settings.API_BASE}session/", {"username": username, "password": password}
    )
    print(response.data)
    assert response.status_code == expected
    if expected == 200:
        assert response.data["key"] is not None


@pytest.mark.django_db
def test_email_verification(anon_client, user):
    client, _ = anon_client
    email, _ = EmailAddress.objects.get_or_create(
        user=user, email=user.email, defaults={"primary": True, "verified": False}
    )
    confirmation = EmailConfirmation.create(email)
    confirmation.sent = timezone.now()
    confirmation.save()
    key = confirmation.key

    response = client.post(f"/{settings.API_BASE}verification/", {"key": key})
    assert response.status_code == 200
    email.refresh_from_db()
    assert email.verified is True


@pytest.mark.django_db
class TestPasswordReset:
    def get_uid_token(self):
        assert len(mail.outbox) == 1
        email_body = mail.outbox[0].body
        matches = re.search(r"http://testserver/reset/(.+?)/(.+?)/", email_body)
        if not matches:
            pytest.fail("Couldn't find uid and token in email")
        return matches.groups()

    def test_password_reset_request(self, anon_client, user):
        client, _ = anon_client
        response = client.post(
            f"/{settings.API_BASE}password-reset/", {"email": user.email}
        )
        assert response.status_code == 200
        assert len(mail.outbox) == 1

    def test_password_reset_request_invalid_email(self, anon_client):
        client, _ = anon_client
        response = client.post(
            f"/{settings.API_BASE}password-reset/", {"email": "nope@not.here"}
        )
        assert response.status_code == 200
        assert len(mail.outbox) == 0

    def test_password_reset_confirm(self, anon_client, user):
        client, _ = anon_client
        client.post(f"/{settings.API_BASE}password-reset/", {"email": user.email})
        uid, token = self.get_uid_token()
        response = client.post(
            f"/{settings.API_BASE}password-reset/",
            {
                "uid": uid,
                "token": token,
                "new_password1": "newpass123",
                "new_password2": "newpass123",
            },
        )
        assert response.status_code == 200

    def test_password_reset_token_invalid_after_use(self, anon_client, user):
        client, _ = anon_client
        self.test_password_reset_confirm(anon_client, user)
        uid, token = self.get_uid_token()
        response = client.post(
            f"/{settings.API_BASE}password-reset/",
            {
                "uid": uid,
                "token": token,
                "new_password1": "newpass123",
                "new_password2": "newpass123",
            },
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestLoginView:
    def test_login_anonymous(self, anon_client):
        client, _ = anon_client
        response = client.get("/login/")
        assert response.status_code == 200
        assert "login.html" in (t.name for t in response.templates)

    def test_login_authenticated(self, user_client):
        client, _ = user_client
        response = client.get("/login/")
        assert response.status_code == 302
        assert response.url == "/"

    def test_login_valid(self, anon_client, user):
        client, _ = anon_client
        response = client.post(
            "/login/",
            {
                "username": user.username,
                "password": "testpass123",
            },
        )
        assert response.status_code == 302
        assert response.url == "/"

    def test_login_invalid(self, anon_client, user):
        client, _ = anon_client
        error = "Please enter a correct username and password."
        response = client.post(
            "/login/",
            {
                "username": user.username,
                "password": "nope",
            },
        )
        assert response.status_code == 200
        assert error in response.content.decode()


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_authenticated(self, user_browser):
        client, _ = user_browser
        assert "_auth_user_id" in client.session
        response = client.post("/logout/")
        assert response.status_code == 302
        assert response.url == "/login/"
        assert "_auth_user_id" not in client.session

    def test_logout_unauthenticated(self, anon_browser):
        client, _ = anon_browser
        assert "_auth_user_id" not in client.session
        response = client.post("/logout/")
        assert response.status_code == 302
        assert response.url == "/login/"
        assert "_auth_user_id" not in client.session
