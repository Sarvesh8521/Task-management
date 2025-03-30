import logging
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from tasks.models import Task
from tasks.serializers import TaskSerializer,CustomExceptionHandler, get_response, success, generic_error
from user_details.models import User


logger = logging.getLogger("django")


def validate_task_data(request_data):
    """
    Validate mandatory fields 
    """
    if not request_data.get("description"):
        raise CustomExceptionHandler({" mandatory"})
    if not request_data.get("project"):
        raise CustomExceptionHandler({" mandatory"})
    if not request_data.get("users"):
        raise CustomExceptionHandler({" required"})
    if request_data.get("status") not in ["To Do", "In Progress", "In Review", "Completed", "Blocked"]:
        raise CustomExceptionHandler({"status": "Invalid status"})
    return True


@transaction.atomic
def create_or_update_task_service(request_data):
    try:
        validate_task_data(request_data)
        
        task_id = request_data.get("id")
        task = Task.objects.filter(id=task_id).first() 
        task = task if task_id else None
        
        if task:
            serializer = TaskSerializer(task, data=request_data, partial=True)
        else:
            serializer = TaskSerializer(data=request_data)
        
        if serializer.is_valid():
            task = serializer.save()
            return get_response(success, TaskSerializer(task).data)
        else:
            raise CustomExceptionHandler(serializer.errors)
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise CustomExceptionHandler(str(e))
    
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
            raise CustomExceptionHandler({" not found"})
        if not user:
            raise CustomExceptionHandler({" not found"})
        if not user.is_active:
            raise CustomExceptionHandler({"not active"})
        
        task.users = user
        task.save()
        return get_response(success, { "Task assigned successfully"})
    
    except Exception as e:
        logger.exception(f"Exception in assign task: {str(e)}")
        raise CustomExceptionHandler("An error occurred")


@transaction.atomic
def delete_task_service(task_id):
    """
   inactive
    """
    try:
        task = Task.objects.filter(id=task_id).first()
        if not task:
            raise CustomExceptionHandler({" not found"})
        
        task.is_active = False
        task.save()
        return get_response(success, {"inactive"})
    
    except Exception as e:
        logger.exception(f"Exception in delete task: {str(e)}")
        raise CustomExceptionHandler("An error occurred ")
    

def get_task_service(task_id):
    """
    Retrieve task details
    """
    try:
        task = Task.objects.filter(id=task_id, is_active=True).first()
        if not task:
            raise CustomExceptionHandler("inactive")
        
        return get_response(success, TaskSerializer(task).data)
    
    except Exception as e:
        logger.exception(f"Exception  {e}")
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
                "count": tasks.count(),
                "results": TaskSerializer(tasks, many=True).data
            }
        )
    
    except Exception as e:
        logger.exception(f"Exception {e}")
        raise CustomExceptionHandler("Error while listing tasks")
