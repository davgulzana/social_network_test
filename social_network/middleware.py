from django.http import JsonResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, "user")
        try:
            auth_res = authentication.JWTAuthentication().authenticate(request)
        except InvalidToken:
            return JsonResponse(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if auth_res:
            request.user = auth_res[0]
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save()
