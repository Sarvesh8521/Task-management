from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import json
import logging

from user_details import User
from user_details.serializers import userserializers

logger = logging.getLogger("django")

@csrf_exempt
@permission_classes([IsAuthenticated])
@swagger_auto_schema (
                     method='post', 
                     request_body=userserializers.ProfileSerializer,
                     operation_id='create_profile'
)


@api_view(['POST'])
def create_profile(request):
    logger.info("create_profile")
    response_data = None

    try:
        serializer = userserializers.ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return JsonResponse(response_data)
        #else:
            #return JsonResponse(serializer.errors)
    except Exception as e:
            logger.exception({e})
            response_data = {'error': 'An error occurred'}
            return JsonResponse(response_data, )
        
    
    except Exception as e:
        logger.exception({e})
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, )
        


@api_view(['GET'])
def get_profile(request):
    logger.info("get_profile")
    response_data = None
    try:
        user = request.user
        profile = user.profile
        serializer = userserializers.ProfileSerializer(profile)
        response_data = serializer.data
        return JsonResponse(response_data)
    except User.DoesNotExist:
        response_data = {'error': 'User not found'}
        return JsonResponse(response_data)
    except Exception as e:
        logger.exception({e})
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, )
    


@api_view(['PUT'])
def update_profile(request):
    logger.info("update_profile")
    response_data = None
    try:
        user = request.user
        profile = user.profile
        serializer = userserializers.ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return JsonResponse(response_data)
        #else:
            #return JsonResponse(serializer.errors)
    except Exception as e:
            logger.exception({e})    
            response_data = {'error': 'An error occurred'}
            return JsonResponse(response_data, )
    except Exception as e:
        logger.exception({e})
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, )
    

@api_view(['DELETE'])
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
        return JsonResponse(response_data)

    except Exception as e:
        logger.exception({e})
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data, )
    

@api_view(['GET'])
def get_all_profiles(request):
    logger.info("get_all_profiles")
    response_data = None
    try:
        profiles = User.objects.all()
        serializer = userserializers.ProfileSerializer(profiles, many=True)
        response_data = serializer.data
        return JsonResponse(response_data)
    except Exception as e:
        logger.exception({e})
        response_data = {'error': 'An error occurred'}
        return JsonResponse(response_data )

