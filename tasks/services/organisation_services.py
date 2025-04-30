import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from tasks.models import Organization
from tasks.serializers import OrganizationSerializer,CustomExceptionHandler,UserNotFoundException,get_response, success


logger = logging.getLogger("django")

@transaction.atomic
def create_or_update_organization_service(request_data):
    try:
        
        organization = Organization.objects.filter(name=request_data.get("name")).first()
        serializer = OrganizationSerializer(instance=organization, data=request_data(organization))
        if serializer.is_valid(raise_exception=True):
            organization = serializer.save()
            return get_response(success, OrganizationSerializer(organization).data)
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise Exception (e.detail)
    
    except Exception as e:
        logger.exception(f"Exception {e}")
        raise CustomExceptionHandler("An error occurred")



@transaction.atomic
def delete_organization_service(organization_id):
    """
    Mark an organization as inactive
    """
    try:
        organization_instance = Organization.objects.filter(id=organization_id).first()
        if not organization_instance:
            raise UserNotFoundException("Organization not found")

        if not organization_instance.is_active:
            raise CustomExceptionHandler("Organization is already inactive")

        organization_instance.is_active = False
        organization_instance.save()
        return get_response(success, {"Organization marked as inactive"})
    
    except Exception as e:
        logger.exception(f"Exception {e}")
        raise CustomExceptionHandler("Error while marking organization as inactive")
