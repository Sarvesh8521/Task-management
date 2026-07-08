import logging

from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


logger = logging.getLogger("django")


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Custom login endpoint that authenticates against Django's auth.User
    and returns JWT tokens along with user info.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return JsonResponse(
            {"error": "Account is disabled."},
            status=status.HTTP_403_FORBIDDEN,
        )

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }, status=status.HTTP_200_OK)
