import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from user_details.models import User
from user_details.serializers.userserializers import UserSerializer

logger = logging.getLogger("django")


@swagger_auto_schema(
    method="post",
    request_body=UserSerializer,
    responses={201: UserSerializer},
    operation_id="Create User",
)
@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    logger.info("POST %s - Create user", request.path)
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Exception in create user: %s", e)
        return JsonResponse({"error": "An error occurred while creating the user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    responses={200: UserSerializer},
    operation_id="Get User",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    logger.info("GET %s - Get user %d", request.path, user_id)
    try:
        user = User.objects.get(id=user_id, is_active=True)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in get user: %s", e)
        return JsonResponse({"error": "An error occurred while retrieving the user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="put",
    request_body=UserSerializer,
    responses={200: UserSerializer},
    operation_id="Update User",
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    logger.info("PUT %s - Update user %d", request.path, user_id)
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in update user: %s", e)
        return JsonResponse({"error": "An error occurred while updating the user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="delete",
    responses={200: openapi.Response(description="User deleted successfully")},
    operation_id="Delete User",
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    logger.info("DELETE %s - Delete user %d", request.path, user_id)
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return JsonResponse({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in delete user: %s", e)
        return JsonResponse({"error": "An error occurred while deleting the user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    responses={200: UserSerializer},
    operation_id="Search Users",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_users(request):
    logger.info("GET %s - Search users", request.path)
    try:
        name = request.GET.get('name')
        email = request.GET.get('email')

        users = User.objects.filter(is_active=True)

        if name:
            users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)
        if email:
            users = users.filter(email_id__icontains=email)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Exception in search users: %s", e)
        return JsonResponse({"error": "An error occurred while searching users."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)