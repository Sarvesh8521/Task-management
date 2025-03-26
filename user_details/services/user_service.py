import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from user_details import serializers as userserializers

from user_details.models import User
from user_details.serializers import UserSerializer
from user_service import UserNotFoundException, UserServiceException
from user_service import success, generic_error
from .user_service import get_response 
from user_service import CustomExceptionHandler


logger = logging.getLogger("django")



def validate_user_data(request_data):
    """
    Validate the mandatory fields for creating or updating a user.
    """
    if not request_data.get("email"):
        raise CustomExceptionHandler({ "Email is mandatory"})
    if not request_data.get("first_name"):
        raise CustomExceptionHandler({"First name is mandatory"})
    if not request_data.get("last_name"):
        raise CustomExceptionHandler({"Last name is mandatory"})
    if not request_data.get("user_id"):
        raise CustomExceptionHandler({"user_id is mandatory"})
    return True


@transaction.atomic
def create_or_update_user_service(request_data):
    try:
        
        validate_user_data(request_data)

        
        unique_identifier =  request_data.get("username")
        
        if not unique_identifier:
            raise CustomExceptionHandler({ "No unique identifier provided"})
        
        user = User.objects.filter( Q(username=unique_identifier)).first()

        if user:
            # Update user details
            user.first_name = request_data.get("first_name")
            user.last_name = request_data.get("last_name")
            user.save()
        else:
            # Create a new user with unique email and username
            if User.objects.filter(email=request_data.get("email")).exists():
                raise CustomExceptionHandler({"Email already exists"})
            if User.objects.filter(username=request_data.get("username")).exists():
                raise CustomExceptionHandler({"Username already exists"})
    
            
            user = User.objects.create_user(
                email=request_data.get("email"),
                first_name=request_data.get("first_name"),
                last_name=request_data.get("last_name"),
            )
        
        user_serializer = UserSerializer(user)
        return get_response(success, user_serializer.data)
    
    except Exception as e:
        logger.exception(f"Exception in create or update user: {e}")
        return get_response(generic_error, CustomExceptionHandler(e))   





@transaction.atomic
def delete_user_service(user_id):
    """
    Marking a user as inactive instead of permanent deletion.
    """
    try:
        if not user_id:
            raise CustomExceptionHandler({ "User ID is mandatory"})
        
        user_instance = User.objects.filter(id=user_id).first()
        if not user_instance:
            raise UserNotFoundException("User not found")
        
        if not user_instance.is_active:
            raise CustomExceptionHandler({ "User is already disabled"})
        
        
        user_instance.is_active = False
        user_instance.save()
        
        return get_response(success, { "User marked as inactive"})
    
    except Exception as e:
        logger.exception(f"Exception in delete_user_service: {e}")
        raise UserServiceException("Error while marking user as inactive")
    



@transaction.atomic
def user_create_service(request_data):
    """
    Creating new users
    """
    try:
        # Validate mandatory fields
        validate_user_data(request_data)

        if User.objects.filter(email=request_data.get("email")).exists():
            raise CustomExceptionHandler({"Email already exists"})
        if User.objects.filter(username=request_data.get("username")).exists():
            raise CustomExceptionHandler({"Username already exists"})

        serializer = userserializers(request_data)
        if not serializer.is_valid():
            raise CustomExceptionHandler({serializer.errors})
        
        user = serializer.save()
        return get_response("User created", userserializers(user).data)
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise CustomExceptionHandler({ str(e)})
    
    except Exception as e:
        logger.exception(f"Exception in user creation: {str(e)}")
        raise CustomExceptionHandler({"An error occurred while creating user"})
    
    


