from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserAccountChangeForm, UserAccountCreationForm
from .models import UserAccount


class UserAccountAdmin(UserAdmin):
    add_form = UserAccountCreationForm
    form = UserAccountChangeForm
    model = UserAccount
    list_display = ["username"]


admin.site.register(UserAccount, UserAccountAdmin)
