from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views import (
    RegisterView,
    ActivationView,
    UserActivityView,
    LoginView,
    ChangePasswordView,
    ForgotPasswordView,
    CreateNewPasswordView,
    ProfileViewSet,
)

user_detail = ProfileViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update"}
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("activate/<uuid:activation_code>/", ActivationView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh_token/", TokenRefreshView.as_view()),
    path("activity/", UserActivityView.as_view()),
    path("change_password/", ChangePasswordView.as_view()),
    path("reset_password/", ForgotPasswordView.as_view()),
    path("reset_password_confirm/", CreateNewPasswordView.as_view()),
    path("profile/", user_detail),
]
