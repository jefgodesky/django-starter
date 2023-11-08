from django.conf import settings
from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    pass

    def __str__(self):
        return self.username

    def can_read(self, other):
        is_public = settings.USER_DETAILS_PUBLIC
        is_auth = other.is_anonymous is False
        has_perm = is_auth and other.has_perm("users.view_useraccount")
        is_self = other.id == self.id
        return is_public or has_perm or other.is_staff or is_self

    def can_delete(self, other):
        has_perm = other.has_perm("users.delete_useraccount")
        is_self = other.id == self.id
        return has_perm or other.is_staff or is_self
