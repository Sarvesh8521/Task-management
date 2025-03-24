from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
import logging

from user_details.models import User
from tasks.models import Organization
from tasks.serializers import OrganizationSerializer
from tasks.serializers import log_info_message, get_response, CustomExceptionHandler, generic_error_2


logger = logging.getLogger("django")

@csrf_exempt
@swagger_auto_schema(
    method="post",
    request_body=OrganizationSerializer,
    responses={201: OrganizationSerializer},
    operation_id="Create Organization"
)
@api_view(["POST"])
def create_organization(request):
    logger.info(log_info_message(request, "Request to create organization"))
    response_obj = None

    try:
        serializer = OrganizationSerializer(request.data)
        if serializer.is_valid():
            organization = serializer.save()
            response_obj = serializer.data
            return JsonResponse(response_obj)
        else:
            return JsonResponse(serializer.errors)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in create organization: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in create organization: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in create organization %s", response_obj)
    return JsonResponse(response_obj)




@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=OrganizationSerializer,
    responses={200: OrganizationSerializer},
    operation_id="Update Organization"
)
@api_view(["PUT"])
def update_organization(request):
    logger.info(log_info_message(request, "Request to update organization with ID: %s"))
    response_obj = None

    try:
        organization = Organization.objects.get(request.data)
        serializer = OrganizationSerializer(organization, data=request.data,)
        if serializer.is_valid():
            organization = serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    except Organization.DoesNotExist:
        response_obj = { "Organization not found."}
        return JsonResponse(response_obj)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in update organization: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in update organization: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in update organization --> %s", response_obj)
    return JsonResponse(response_obj)