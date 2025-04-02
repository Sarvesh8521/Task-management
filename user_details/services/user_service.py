import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from user_details.serializers import UserSerializer
from user_details.models import User
from user_service import CustomExceptionHandler, UserNotFoundException, UserServiceException
from user_service import success, generic_error
from .user_service import get_response

logger = logging.getLogger("django")


@transaction.atomic
def create_or_update_user_service(request_data):
    """
    Create or update a user with validation handled in the serializer.
    """
    try:
        user = User.objects.filter(username=request_data.get("username")).first()
        
        serializer = UserSerializer(instance=user, data=request_data(user))
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return get_response(success, serializer.data)

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise CustomExceptionHandler({"error": str(e)})

    except Exception as e:
        logger.exception(f"Exception in create_or_update_user_service: {e}")
        return get_response(generic_error, {"error": str(e)})


@transaction.atomic
def delete_user_service(user_id):
    """
    Marking a user as inactive.
    """
    try:
        if not user_id:
            raise CustomExceptionHandler({"User ID is mandatory"})
        
        user_instance = User.objects.filter(id=user_id).first()
        if not user_instance:
            raise UserNotFoundException({"User not found"})
        
        if not user_instance.is_active:
            raise CustomExceptionHandler({ "User is already disabled"})
        
        user_instance.is_active = False
        user_instance.save()
        
        return get_response(success, {"User marked as inactive"})
    
    except Exception as e:
        logger.exception(f"Exception in delete_user_service: {e}")
        raise UserServiceException("Error while marking user as inactive")




# @transaction.atomic
# def user_create_service(request_data):
#     """
#     Creating new users with validation at the serializer level.
#     """
#     try:
#         serializer = UserSerializer(data=request_data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             return get_response(success, serializer.data)

#     except ValidationError as e:
#         logger.error(f"Validation error: {str(e)}")
#         raise CustomExceptionHandler({" str(e)})

#     except Exception as e:
#         logger.exception(f"Exception in user_create_service: {e}")
#         raise CustomExceptionHandler({"An error occurred while creating user"})
