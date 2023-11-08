import pytest

from .models import UserAccount
from .serializers import UserSerializer


@pytest.fixture
def user():
    return UserAccount.objects.create_user(username="tester", password="testpass123")


@pytest.mark.django_db
class TestUserSerializerSerialization:
    @pytest.fixture(autouse=True)
    def setup_method(self, verified_user):
        self.serializer = UserSerializer(verified_user)

    @pytest.mark.parametrize(
        "field, value",
        [
            ("id", lambda user: user.id),
            ("username", lambda user: user.username),
            ("is_active", lambda user: user.is_active),
            ("is_staff", lambda user: user.is_staff),
        ],
    )
    def test_user_serializer_fields(self, verified_user, field, value):
        assert self.serializer.data[field] == value(verified_user)


@pytest.mark.django_db
class TestUserSerializerDeserialization:
    def test_create_user(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        serializer.save()
        assert UserAccount.objects.filter(username="newuser").exists()

    def test_update_user(self, verified_user):
        update = {
            "username": "updateduser",
        }
        serializer = UserSerializer(verified_user, data=update, partial=True)
        assert serializer.is_valid()
        serializer.save()
        verified_user.refresh_from_db()
        assert verified_user.username == "updateduser"

    def test_invalid_data(self):
        data = {"nope": True}
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
