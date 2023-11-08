import pytest
from django.contrib.auth.models import Permission
from django.test import override_settings


@pytest.mark.django_db
class TestUserAccountConstructor:
    def test_user_account_username(self, verified_user):
        assert verified_user.username == "user"

    def test_user_account_email(self, verified_user):
        assert verified_user.email == "user@testing.com"

    def test_user_account_str(self, verified_user):
        assert str(verified_user.username) == "user"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_user, public, has_perm, expected",
    [
        ("anon", True, False, True),
        ("anon", False, False, False),
        ("other", True, True, True),
        ("other", False, True, True),
        ("other", True, False, True),
        ("other", False, False, False),
        ("user", True, True, True),
        ("user", False, True, True),
        ("user", True, False, True),
        ("user", False, False, True),
        ("staff", True, True, True),
        ("staff", False, True, True),
        ("staff", True, False, True),
        ("staff", False, False, True),
    ],
    indirect=["get_user"],
)
def test_can_read(get_user, verified_user, public, has_perm, expected):
    with override_settings(USER_DETAILS_PUBLIC=public):
        if has_perm:
            permission = Permission.objects.get(codename="view_useraccount")
            get_user.user_permissions.add(permission)
        assert verified_user.can_read(get_user) == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_user, has_perm, expected",
    [
        ("anon", False, False),
        ("other", False, False),
        ("other", True, True),
        ("user", False, True),
        ("user", True, True),
        ("staff", False, True),
        ("staff", True, True),
    ],
    indirect=["get_user"],
)
def test_can_delete(get_user, verified_user, has_perm, expected):
    if has_perm:
        permission = Permission.objects.get(codename="delete_useraccount")
        get_user.user_permissions.add(permission)
    assert verified_user.can_delete(get_user) == expected
