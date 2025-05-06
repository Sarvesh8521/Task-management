from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
from user_details.models import User
from tasks.models import Organization
from tasks.serializers import OrganizationSerializer



logger = logging.getLogger("django")

@csrf_exempt
@swagger_auto_schema(
    method="post",
    request_body=OrganizationSerializer,
    responses={201: OrganizationSerializer},
    operation_id="Create Organization"
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_organization(request):
    logger.info("create organization")
    
    try:
        data = request.data.copy()
        data["super_user"] = request.user.id
        serializer = OrganizationSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(super_user=request.user.id)  
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({'error': 'An error occurred while creating organization'})
    


@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=OrganizationSerializer,
    responses={200: OrganizationSerializer},
    operation_id="Update Organization"
)
@api_view(["PUT"])
def update_organization(request, org_id):
    logger.info("Request to update organization")
    try:
        organization = Organization.objects.get(id=org_id)
        if organization.super_user != request.user.id:
            return JsonResponse({"error": "You don't have permission to update this organization"},status=status.HTTP_403_FORBIDDEN)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors)
    except Organization.DoesNotExist:
        return JsonResponse({"error": "Organization not found"})
    except Exception as e:
        logger.exception(f"Exception in update organization: {e}")
        return JsonResponse({"error": "An error occurred while updating organization"})
    


@csrf_exempt
@swagger_auto_schema(
    method="delete",
    responses={200: OrganizationSerializer},
    request_body=OrganizationSerializer,
    operation_id="Delete Organization"
)
@api_view(["DELETE"])
def delete_organization(request, org_id):
    logger.info("Request to delete organization")
    try:
        organization = Organization.objects.get(id=org_id)
        if organization.super_user != request.user.id:
            return JsonResponse({"error": "You don't have permission to delete this organization"},status=status.HTTP_403_FORBIDDEN)
        organization.delete()
        return JsonResponse({"message": "Organization deleted"})
    except Organization.DoesNotExist:
        return JsonResponse({"error": "Organization not found"})
    except Exception as e:
        logger.exception(f"Exception in delete organization: {e}")
        return JsonResponse({"error": "An error occurred while deleting organization"})


@csrf_exempt
@swagger_auto_schema(
    method="get",
    responses={200: OrganizationSerializer},
    # request_body=OrganizationSerializer,
    operation_id="Get Organization"
)
@api_view(["GET"])
def get_organization(request, org_id):    
    logger.info("Request to get organization")
    try:
        organization = Organization.objects.get(id=org_id)
        serializer = OrganizationSerializer(organization)
        return JsonResponse(serializer.data)
    except Organization.DoesNotExist:
        return JsonResponse({"error": "Organization not found"})
    except Exception as e:
        logger.exception(f"Exception in get organization: {e}")
        return JsonResponse({"error": "An error occurred while getting organization"})