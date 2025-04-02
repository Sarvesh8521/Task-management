import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from tasks.models import Project
from tasks.serializers import ProjectSerializer
from tasks.serializers import get_response, CustomExceptionHandler, UserNotFoundException, UserServiceException, success, generic_error

logger = logging.getLogger("django")

@transaction.atomic
def create_or_update_project_service(request_data):
    try:
        project = Project.objects.filter(name=request_data.get("name")).first()

        serializer = ProjectSerializer(instance=project, data=request_data(project))
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            return get_response(success, ProjectSerializer(project).data)

    except Exception as e:
        logger.exception(f"Exception {e}")
        return get_response(generic_error, {"error": str(e)})
    




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
            raise UserNotFoundException("Project not found")

        if not project_instance.is_active:
            raise CustomExceptionHandler({ "Project already inactive"})

        project_instance.is_active = False
        project_instance.save()

        return get_response(success, { "Project marked as inactive"})

    except Exception as e:
        logger.exception(f"Exception in delete_project_service: {e}")
        raise UserServiceException("Error while marking project as inactive")
    



def get_project_service(project_id):
    """
    Retrieve project details
    """
    try:
        project = Project.objects.filter(id=project_id, is_active=True).first()
        if not project:
            raise CustomExceptionHandler({ "Project not found or inactive"})
        
        return get_response(success, ProjectSerializer(project).data)
    
    except Exception as e:
        logger.exception(f"Exception in get_project_service: {e}")
        raise CustomExceptionHandler({ "Error retrieving project"})
    
    

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
        raise CustomExceptionHandler({"Error while listing projects"})
 