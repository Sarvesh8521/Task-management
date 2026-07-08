import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from tasks.models import Organization
from tasks.serializers import OrganizationSerializer

logger = logging.getLogger("django")


@swagger_auto_schema(
    method="post",
    request_body=OrganizationSerializer,
    responses={201: OrganizationSerializer},
    operation_id="Create Organization",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_organization(request):
    logger.info("POST %s - Create organization", request.path)
    try:
        data = request.data.copy()
        data["super_user"] = request.user.id
        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Exception in create organization: %s", e)
        return JsonResponse({"error": "An error occurred while creating the organization."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="put",
    request_body=OrganizationSerializer,
    responses={200: OrganizationSerializer},
    operation_id="Update Organization",
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_organization(request, org_id):
    logger.info("PUT %s - Update organization %d", request.path, org_id)
    try:
        organization = Organization.objects.get(id=org_id)
        if organization.super_user != request.user.id:
            return JsonResponse(
                {"error": "You don't have permission to update this organization."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = OrganizationSerializer(organization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Organization.DoesNotExist:
        return JsonResponse({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in update organization: %s", e)
        return JsonResponse({"error": "An error occurred while updating the organization."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="delete",
    operation_id="Delete Organization",
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_organization(request, org_id):
    logger.info("DELETE %s - Delete organization %d", request.path, org_id)
    try:
        organization = Organization.objects.get(id=org_id)
        if organization.super_user != request.user.id:
            return JsonResponse(
                {"error": "You don't have permission to delete this organization."},
                status=status.HTTP_403_FORBIDDEN,
            )
        organization.is_active = False
        organization.save()
        return JsonResponse({"message": "Organization deleted successfully."}, status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
        return JsonResponse({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in delete organization: %s", e)
        return JsonResponse({"error": "An error occurred while deleting the organization."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    responses={200: OrganizationSerializer},
    operation_id="Get Organization",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_organization(request, org_id):
    logger.info("GET %s - Get organization %d", request.path, org_id)
    try:
        organization = Organization.objects.get(id=org_id, is_active=True)
        serializer = OrganizationSerializer(organization)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
        return JsonResponse({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in get organization: %s", e)
        return JsonResponse({"error": "An error occurred while retrieving the organization."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)