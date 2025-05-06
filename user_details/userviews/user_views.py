from django.conf import settings
if not settings.configured:
    settings.configure()

from drf_yasg import openapi
# In user_views.py, add:
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import logging

from user_details.models import User
from user_details.serializers.userserializers import UserSerializer

logger = logging.getLogger("django")


@csrf_exempt
@swagger_auto_schema(
    method="post",
    request_body=UserSerializer,
    responses={200: UserSerializer},
    operation_id="Create User"
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user(request):
    logger.info("create user: %s", request.data)
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)
    except Exception as e:
        logger.exception(f"Exception in create user: {e}")
        return JsonResponse({"error": "An error occurred while creating the user."})


@csrf_exempt
@swagger_auto_schema(
    method="get",
    responses={200: UserSerializer},
    operation_id="Get User"
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    logger.info("Request to get user with ID: %s", user_id)
    try:
        name = request.GET.get('name')
        organization = request.GET.get('organization')
        email = request.GET.get('email')

        users = User.objects.all()

        if name:
            users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)
        if organization:
            users = users.filter(profile__organization__icontains=organization)
        if email:
            users = users.filter(email__icontains=email)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        logger.exception(f"Exception in get user: {e}")
        return JsonResponse({"error": "An error occurred while retrieving the user."}, status=500)


@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=UserSerializer,
    responses={201: UserSerializer},
    operation_id="Update User"
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    logger.info("Request to update user with ID: %s", user_id)
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, status=400, safe=False)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        logger.exception(f"Exception in update user: {e}")
        return JsonResponse({"error": "An error occurred while updating the user."}, status=500)


@csrf_exempt
@swagger_auto_schema(
    method="delete",
    responses={204: openapi.Response(description="User deleted successfully")},
    operation_id="Delete User"
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    logger.info("delete user with ID: %s", user_id)
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully."}, status=204)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        logger.exception(f"Exception in delete user: {e}")
        return JsonResponse({"error": "An error occurred while deleting the user."}, status=500)
    

@csrf_exempt
@swagger_auto_schema(
    method="search",
    responses={200: UserSerializer},
    operation_id="Search User"
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_user(request):
    logger.info("Request to search user")
    try:
        name = request.GET.get('name')
        organization = request.GET.get('organization')
        email = request.GET.get('email')

        users = User.objects.all()

        if name:
            users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)
        if organization:
            users = users.filter(profile__organization__icontains=organization)
        if email:
            users = users.filter(email__icontains=email)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        logger.exception(f"Exception in search user: {e}")
        return JsonResponse({"error": "An error occurred while searching the user."}, status=500)