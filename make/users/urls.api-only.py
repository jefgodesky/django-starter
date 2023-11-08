from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings
from django.urls import path

from .views import PasswordResetPostView, SessionAPIView, UserAPIView, UserDetailAPIView

API_BASE = settings.API_BASE
users_api = f"{API_BASE}users/"
session_api = f"{API_BASE}session/"
verify_api = f"{API_BASE}verification/"
reset_api = f"{API_BASE}password-reset/"

urlpatterns = [
    path(users_api, UserAPIView.as_view(), name="user_coll_api"),
    path(f"{users_api}<int:pk>/", UserDetailAPIView.as_view(), name="user_detail_api"),
    path(session_api, SessionAPIView.as_view(), name="session_api"),
    path(
        f"{verify_api}",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        f"{verify_api}/<str:key>",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(reset_api, PasswordResetPostView.as_view(), name="password_reset_api"),
]
