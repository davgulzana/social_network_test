from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, mixins, viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from account.serializers import (
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ProfileSerializer,
)
from account.utils import send_activation_mail, send_reset_password_mail

User = get_user_model()


class RegisterView(APIView):
    permission_classes = []

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_mail(user)
            return Response(
                "User successfully registered", status=status.HTTP_201_CREATED
            )


class ActivationView(APIView):
    """
    View for activation email of user.
    """

    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ""
        user.save()
        return Response(
            "Your account successfully activated", status=status.HTTP_200_OK
        )


class LoginView(TokenViewBase):
    serializer_class = LoginSerializer


class UserActivityView(APIView):
    """
    View for get information about user activity.
    Returns last_login (when the user logged last time)
    and last_activity (when the user made the last request to the service).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "last_login": request.user.last_login,
            "last_activity": request.user.last_activity,
        }
        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Password updated successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        try:
            user = User.objects.get(email=email)
            send_reset_password_mail(user)
            return Response(
                "Check your email. Password recovery code sanded.",
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response("USER_DOES_NOT_EXIST", status=status.HTTP_404_NOT_FOUND)


class CreateNewPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data.get("activation_code")
            password = serializer.validated_data.get("new_password")
            user = User.objects.get(activation_code=code)
            user.activation_code = ""
            user.is_active = True
            user.set_password(password)
            user.save()
            return Response("Password changed successfully", status=status.HTTP_200_OK)


class ProfileViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
