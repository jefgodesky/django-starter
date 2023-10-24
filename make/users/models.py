from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    pass

    def __str__(self):
        return self.username
