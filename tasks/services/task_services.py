import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from tasks.models import Task
from tasks.serializers import TaskSerializer, CustomExceptionHandler, get_response, success, generic_error
from user_details.models import User

logger = logging.getLogger("django")

@transaction.atomic
def create_or_update_task_service(request_data):
    try:
        task_id = request_data.get("id")
        task = Task.objects.filter(id=task_id).first() if task_id else None
        
        serializer = TaskSerializer(instance=task, data=request_data(task))
        if serializer.is_valid(raise_exception=True):
            task = serializer.save()
            return get_response(success, TaskSerializer(task).data)
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise CustomExceptionHandler(e.detail)
    
    except Exception as e:
        logger.exception(f"Exception {str(e)}")
        raise CustomExceptionHandler("An error occurred")
    



@transaction.atomic
def assign_task_service(task_id, user_id):
    """
    Assign a task to a user
    """
    try:
        task = Task.objects.filter(id=task_id).first()
        user = User.objects.filter(id=user_id).first()
        
        if not task:
            raise CustomExceptionHandler({ "Task not found"})
        if not user:
            raise CustomExceptionHandler({"User not found"})
        if not user.is_active:
            raise CustomExceptionHandler({ "User is not active"})
        
        task.users.add(user)
        task.save()
        return get_response(success, { "Task assigned successfully"})
    
    except Exception as e:
        logger.exception(f"Exception in assign task: {str(e)}")
        raise CustomExceptionHandler("An error occurred")



@transaction.atomic
def delete_task_service(task_id):
    """
    Mark a task as inactive
    """
    try:
        task = Task.objects.filter(id=task_id).first()
        if not task:
            raise CustomExceptionHandler({"Task not found"})
        
        task.is_active = False
        task.save()
        return get_response(success, {"Task marked as inactive"})
    
    except Exception as e:
        logger.exception(f"Exception in delete task: {str(e)}")
        raise CustomExceptionHandler("An error occurred")


def get_task_service(task_id):
    """
    Retrieve task details
    """
    try:
        task = Task.objects.filter(id=task_id, is_active=True).first()
        if not task:
            raise CustomExceptionHandler("Task is inactive or not found")
        
        return get_response(success, TaskSerializer(task).data)
    
    except Exception as e:
        logger.exception(f"Exception {e}")
        raise CustomExceptionHandler("Error while retrieving task")
    



def list_tasks_service(filters=None):
    """
    List all active tasks with optional filters
    """
    try:
        queryset = Task.objects.filter(is_active=True)
        
        if filters:
            if filters.get("project"):
                queryset = queryset.filter(project_id=filters["project"])
            if filters.get("status"):
                queryset = queryset.filter(status=filters["status"])
            if filters.get("user"):
                queryset = queryset.filter(users__id=filters["user"])
            if filters.get("search"):
                queryset = queryset.filter(
                    Q(description__icontains=filters["search"]) |
                    Q(release_version__icontains=filters["search"])
                )
        
        tasks = queryset.order_by('-creation_date')
        return get_response(
            success, 
            {
                 tasks.count(),
                 TaskSerializer(tasks, many=True).data
            }
        )
    
    except Exception as e:
        logger.exception(f"Exception {e}")
        raise CustomExceptionHandler("Error while listing tasks")
