from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView as APILoginView
from dj_rest_auth.views import LogoutView as APILogoutView
from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserAccountCreationForm
from .models import UserAccount
from .serializers import UserSerializer


class UserRegisterAPIView(RegisterView):
    def get_response_data(self, user):
        return UserSerializer(user).data


class UserDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)

        if user.can_read(request.user):
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif not request.user.is_authenticated:
            raise NotAuthenticated
        else:
            raise PermissionDenied

    def delete(self, request, pk):
        user = self.get_object(pk)

        if user.can_delete(request.user):
            user.is_active = False
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif not request.user.is_authenticated:
            raise NotAuthenticated
        else:
            raise PermissionDenied


class UserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        view = prepare_view(UserRegisterAPIView(), self)
        return view.post(request, *args, **kwargs)


class SessionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        view = prepare_view(APILoginView(), self)
        return view.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        view = prepare_view(APILogoutView(), self)
        return view.post(request, *args, **kwargs)


class RegisterFormView(CreateView):
    form_class = UserAccountCreationForm
    success_url = reverse_lazy("login")
    template_name = "register.html"


class LoginFormView(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class PasswordResetPostView(View):
    def post(self, request, *args, **kwargs):
        if "email" in request.POST:
            return PasswordResetView.as_view()(request, *args, **kwargs)
        elif all(
            key in request.POST
            for key in ["new_password1", "new_password2", "uid", "token"]
        ):
            return PasswordResetConfirmView.as_view()(request, *args, **kwargs)
        else:
            msg = "Invalid request data for password reset."
            return JsonResponse({"error": msg}, status=400)


def prepare_view(view, context):
    view.request = context.request
    view.format_kwarg = context.format_kwarg
    view.args = context.args
    view.kwargs = context.kwargs
    return view
