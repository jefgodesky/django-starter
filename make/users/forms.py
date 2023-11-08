from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import UserAccount


class UserAccountCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ("username",)


class UserAccountChangeForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ("username",)
