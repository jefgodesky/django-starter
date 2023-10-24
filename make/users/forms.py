from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class UserAccountCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "username"


class UserAccountChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "username"
