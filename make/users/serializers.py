from rest_framework import serializers

from .models import UserAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("id", "username", "is_active", "is_staff")
