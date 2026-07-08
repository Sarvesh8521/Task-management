import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from user_details.models import Profile
from user_details.serializers.profileserializers import ProfileSerializer

logger = logging.getLogger("django")


@swagger_auto_schema(
    method="post",
    request_body=ProfileSerializer,
    responses={201: ProfileSerializer},
    operation_id="Create Profile",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_profile(request):
    logger.info("POST %s - Create profile", request.path)
    try:
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Exception in create profile: %s", e)
        return JsonResponse({"error": "An error occurred while creating the profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    responses={200: ProfileSerializer},
    operation_id="Get Profile",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request, user_id):
    logger.info("GET %s - Get profile for user %d", request.path, user_id)
    try:
        profile = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in get profile: %s", e)
        return JsonResponse({"error": "An error occurred while retrieving the profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="put",
    request_body=ProfileSerializer,
    responses={200: ProfileSerializer},
    operation_id="Update Profile",
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request, user_id):
    logger.info("PUT %s - Update profile for user %d", request.path, user_id)
    try:
        profile = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in update profile: %s", e)
        return JsonResponse({"error": "An error occurred while updating the profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="delete",
    operation_id="Delete Profile",
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_profile(request, user_id):
    logger.info("DELETE %s - Delete profile for user %d", request.path, user_id)
    try:
        profile = Profile.objects.get(user_id=user_id)
        profile.delete()
        return JsonResponse({"message": "Profile deleted successfully."}, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in delete profile: %s", e)
        return JsonResponse({"error": "An error occurred while deleting the profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
