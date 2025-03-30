import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from tasks.models import Project
from tasks.serializers import ProjectSerializer 

from tasks.serializers import get_response, CustomExceptionHandler,UserNotFoundException, UserServiceException,success, generic_error

logger = logging.getLogger("django")

def validate_project_data(request_data):
    """
    Validate the mandatory fields
    """
    if not request_data.get("name"):
        raise CustomExceptionHandler({" mandatory"})
    if not request_data.get("super_user"):
        raise CustomExceptionHandler({" mandatory"})
    if not request_data.get("status"):
        raise CustomExceptionHandler({"mandatory"})
    if not request_data.get("sprint"):
        raise CustomExceptionHandler({" mandatory"})
    return True

@transaction.atomic
def create_or_update_project_service(request_data):
    try:
        validate_project_data(request_data)

        
        project = Project.objects.filter(name=request_data.get("name")).first()

        if project:
            
            project.super_user = request_data.get(project.super_user)
            project.sub_user = request_data.get( project.sub_user)
            project.users = request_data.get( project.users)
            project.status = request_data.get( project.status)
            project.start_date = request_data.get( project.start_date)
            project.end_date = request_data.get( project.end_date)
            project.release_version = request_data.get(project.release_version)
            project.sprint = request_data.get(project.sprint)
            project.save()
        else:
            
            project = Project.objects.create(
                name=request_data.get("name"),
                super_user=request_data.get("super_user"),
                sub_user=request_data.get("sub_user"),
                users=request_data.get("users"),
                status=request_data.get("status"),
                start_date=request_data.get("start_date"),
                end_date=request_data.get("end_date"),
                release_version=request_data.get("release_version"),
                sprint=request_data.get("sprint"),
            )

        project_serializer = ProjectSerializer(project)
        return get_response(success, project_serializer.data)

    except Exception as e:
        logger.exception(f"Exception {e}")
        return get_response(generic_error, CustomExceptionHandler(e))



@transaction.atomic
def delete_project_service(project_id):
    """
    Marking a project as inactive 
    """
    try:
        if not project_id:
            raise CustomExceptionHandler({"Project ID is mandatory"})

        project_instance = Project.objects.filter(id=project_id).first()
        if not project_instance:
            raise UserNotFoundException("not found")

        if not project_instance.is_active:
            raise CustomExceptionHandler({" already inactive"})

        project_instance.is_active = False
        project_instance.save()

        return get_response(success, {" marked as inactive"})

    except Exception as e:
        logger.exception(f"Exception in delete_project_service: {e}")
        raise UserServiceException("Error while marking project as inactive")

@transaction.atomic
def project_create_service(request_data):
    """
    Creating new projects
    """
    try:
        
        validate_project_data(request_data)

        if Project.objects.filter(name=request_data.get("name")).exists():
            raise CustomExceptionHandler({"P name already exists"})

        serializer = ProjectSerializer(data=request_data)
        if not serializer.is_valid():
            raise CustomExceptionHandler({serializer.errors})

        project = serializer.save()
        return get_response(" created", ProjectSerializer(project).data)

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise CustomExceptionHandler({"error": str(e)})

    except Exception as e:
        logger.exception(f"Exception in project creation: {str(e)}")
        raise CustomExceptionHandler({"An error while creating"})
    


def get_project_service(project_id):
    """
    Retrieve project details
    """
    try:
        project = Project.objects.filter(id=project_id, is_active=True).first()
        if not project:
            raise CustomExceptionHandler(" not found or inactive")
        
        return get_response(success, ProjectSerializer(project).data)
    
    except Exception as e:
        logger.exception(f"Exception in get_project_service: {e}")
        raise   CustomExceptionHandler("Error")

def list_projects_service(filters=None):
    """
    List all active projects 
    """
    try:
        queryset = Project.objects.filter(is_active=True)
        
        if filters:
            if filters.get("status"):
                queryset = queryset.filter(status=filters["status"])
            if filters.get("super_user"):
                queryset = queryset.filter(super_user_id=filters["super_user"])
        
        projects = queryset.order_by('creation_date')
        return get_response(
            success, 
            {
                 projects.count(),
                 ProjectSerializer(projects, many=True).data
            }
        )
    
    except Exception as e:
        logger.exception(f"Exception in list_projects_service: {e}")
        raise CustomExceptionHandler("Error while listing projects")