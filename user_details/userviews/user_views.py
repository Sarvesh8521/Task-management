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
@swagger_auto_schema(method="post",
                     request_body=userserializers,
                     responses={200: userserializers},
                     operation_id="Create User"
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user(request):
    logger.info (" create user: %s", request.data)
    response_obj = None

    try:
        serializer = userserializers(request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_obj = serializer.data
            return JsonResponse(response_obj)
        else:
            return JsonResponse(serializer.errors)

    except Exception as e:
        logger.exception(f"Exception in create user: {e}")
        response_obj = {"An error occurred while creating the user."}
        return JsonResponse(response_obj)



@csrf_exempt
@swagger_auto_schema(
    method="get",
    responses={200: userserializers},
    operation_id="Get User"
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    logger.info("Request to get user with ID: %s", user_id)
    response_obj = None

    try:
        name = request.GET.get('name')
        organization = request.GET.get('organization')
        email = request.GET.get('email')

        
        user = User.objects.all()
        if name:
            users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)
        if organization:
            users = users.filter(profile__organization__icontains=organization)
        if email:
            users = users.filter(email_id__icontains=email)

        #user = User.objects.get(user_id=user_id)
        serializer = userserializers(user)
        return JsonResponse(serializer.data)

    except User.DoesNotExist:
        response_obj = { "User  not found."}
        return JsonResponse(response_obj)

    except Exception as e:
        logger.exception(f"Exception in get user: {e}")
        response_obj = { "An error occurred while retrieving the user."}
        return JsonResponse(response_obj)




@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=userserializers,
    responses={201: userserializers},
    operation_id="Update User"
)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    logger.info("Request to update user with ID: %s", user_id)
    response_obj = None

    try:
        user = User.objects.get(user_id)
        serializer = userserializers(user, data=request.data,)
        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    except User.DoesNotExist:
        response_obj = { "User  not found."}
        return JsonResponse(response_obj)

    except Exception as e:
        logger.exception(f"Exception in update user: {e}")
        response_obj = {" error  while updating"}
        return JsonResponse(response_obj)




@csrf_exempt
@swagger_auto_schema(
    method="delete",
    responses={204: openapi.Response(description="User  deleted successfully")},
    operation_id="Delete User"
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])

def delete_user(request, user_id):
    logger.info("delete user with ID: %s", user_id)
    response_obj = None

    try:
        user = User.objects.get(user_id=user_id)
        user.delete()
        return JsonResponse({})

    except User.DoesNotExist:
        response_obj = {"User  not found."}
        return JsonResponse(response_obj)

    except Exception as e:
        logger.exception(f"Exception in delete user: {e}")
        response_obj = {"An error occurred while deleting "}
        return JsonResponse(response_obj)