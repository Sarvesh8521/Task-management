import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from user_details.models import User
from tasks.models import Organization
from tasks.serializers import OrganizationSerializer,CustomExceptionHandler, UserNotFoundException, generic_error,get_response,success
from user_details import UserServiceException




logger = logging.getLogger("django")

def validate_organization_data(request_data):
    """
    Validate the fields 
    """
    if not request_data.get("name"):
        raise CustomExceptionHandler({"Organization name is mandatory"})
    if not request_data.get("super_user"):
        raise CustomExceptionHandler({"Super user is mandatory"})
    if request_data.get("super_user") == request_data.get("sub_user"):
        raise CustomExceptionHandler({"user cannot be the same"})
    return True

@transaction.atomic
def create_or_update_organization_service(request_data):
    try:
        validate_organization_data(request_data)
        
        organization = Organization.objects.filter(Q(name=request_data.get("name"))).first()
        
        if organization:
            organization.super_user = request_data.get("super_user")
            organization.sub_user = request_data.get("sub_user")
            organization.save()
        else:
            if Organization.objects.filter(name=request_data.get("name")).exists():
                raise CustomExceptionHandler({"Organization name already exists"})
            
            organization = Organization.objects.create(
                name=request_data.get("name"),
                super_user=request_data.get("super_user"),
                sub_user=request_data.get("sub_user"),
            )
        
        organization_serializer = OrganizationSerializer(organization)
        return get_response(success, organization_serializer.data)
    
    except Exception as e:
        logger.exception(f"Exception {e}")
        return get_response(generic_error, CustomExceptionHandler(e))

@transaction.atomic
def delete_organization_service(organization_id):
    """
    Marking an organization as inactive
    """
    try:
        if not organization_id:
            raise CustomExceptionHandler({"Organization ID is mandatory"})
        
        organization_instance = Organization.objects.filter(id=organization_id).first()
        if not organization_instance:
            raise UserNotFoundException(" not found")
        
        if not organization_instance.is_active:
            raise CustomExceptionHandler({" already disabled"})
        
        organization_instance.is_active = False
        organization_instance.save()
        
        return get_response(success, {" marked as inactive"})
    
    except Exception as e:
        logger.exception(f"Exception {e}")
        raise UserServiceException("Error while marking organization as inactive")



@transaction.atomic
def organization_create_service(request_data):
    """
    Creating new organizations
    """
    try:
        validate_organization_data(request_data)
        
        if Organization.objects.filter(name=request_data.get("name")).exists():
            raise CustomExceptionHandler({"Organization name already exists"})
        
        serializer = OrganizationSerializer(data=request_data)
        if not serializer.is_valid():
            raise CustomExceptionHandler(serializer.errors)
        
        organization = serializer.save()
        return get_response("Organization created", OrganizationSerializer(organization).data)
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise CustomExceptionHandler(str(e))
    
    except Exception as e:
        logger.exception(f"Exception in organization creation: {str(e)}")
        raise CustomExceptionHandler("An error occurred while creating organization")
