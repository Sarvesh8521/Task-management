from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import logging

from user_details.models import User
from tasks.models import Organization
from tasks.serializers.organizationserializers import OrganizationSerializer

logger = logging.getLogger("django")

@csrf_exempt
@swagger_auto_schema(
    method="post",
    request_body=organizationserializer,
    responses={201: Organizationserializer},
    operation_id="Create Organization"
)
@api_view(["POST"])
def create_organization(request):
    logger.info(log_info_message(request, "Request to create organization"))
    response_obj = None

    try:
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            response_obj = serializer.data
            return JsonResponse(response_obj, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in create organization: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in create organization: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in create organization --> %s", response_obj)
    return JsonResponse(response_obj, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=OrganizationSerializer,
    responses={200: OrganizationSerializer},
    operation_id="Update Organization"
)
@api_view(["PUT"])
def update_organization(request, org_id):
    logger.info(log_info_message(request, "Request to update organization with ID: %s", org_id))
    response_obj = None

    try:
        organization = Organization.objects.get(id=org_id)
        serializer = OrganizationSerializer(organization, data=request.data, partial=True)
        if serializer.is_valid():
            organization = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Organization.DoesNotExist:
        response_obj = {"error": "Organization not found."}
        return JsonResponse(response_obj, status=status.HTTP_404_NOT_FOUND)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in update organization: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in update organization: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in update organization --> %s", response_obj)
    return JsonResponse(response_obj, status=status.HTTP_500_INTERNAL_SERVER_ERROR)