from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
from user_details.models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import json
import logging
from user_details.models import User
from user_details.serializers import userserializers
from user_details.serializers.profileserializers import ProfileSerializer

logger = logging.getLogger("django")


@csrf_exempt
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method='post',
    request_body=ProfileSerializer,
    operation_id='create_profile'
)
@api_view(['POST'])
def create_profile(request):
    logger.info("create_profile")
    response_data = None

    try:
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return JsonResponse(response_data, safe=False)
        else:
            return JsonResponse(serializer.errors)

    except Exception as e:
        logger.exception(e)
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, status=500)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    logger.info("get_profile")
    response_data = None
    try:
        user = request.user
        profile = user.profile
        serializer = ProfileSerializer(profile)
        response_data = serializer.data
        return JsonResponse(response_data, safe=False)
    except User.DoesNotExist:
        response_data = {'error': 'User not found'}
        return JsonResponse(response_data, status=404)
    except Exception as e:
        logger.exception(e)
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, status=500)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request,user_id):
    try:
        # Get the profile for the specified user
        profile = Profile.objects.get(user_id=user_id)
        
        # Update the profile with request data
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
        
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)
    except Exception as e:
        logger.exception(f"Exception in update profile: {e}")
        return JsonResponse({"error": str(e)}, status=500)


    # logger.info("update_profile")
    # response_data = None
    # try:
    #     user = request.user
    #     profile = user.profile
    #     serializer = ProfileSerializer(profile, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response_data = serializer.data
    #         return JsonResponse(response_data, safe=False)
    #     else:
    #         return JsonResponse(serializer.errors, status=400, safe=False)
    # except Exception as e:
    #     logger.exception(e)
    #     response_data = {'error': 'An error occurred'}
    #     return JsonResponse(response_data, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    logger.info("delete_profile")
    response_data = None
    try:
        user = request.user
        profile = user.profile
        profile.delete()
        response_data = {'message': 'Profile deleted'}
        return JsonResponse(response_data)
    except User.DoesNotExist:
        response_data = {'error': 'User not found'}
        return JsonResponse(response_data, status=404)
    except Exception as e:
        logger.exception(e)
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_profiles(request):
    logger.info("get_all_profiles")
    response_data = None
    try:
        profiles = User.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        response_data = serializer.data
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        logger.exception(e)
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, status=500)
