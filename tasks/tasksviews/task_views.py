from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
import logging
import json

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.serializers import get_response, CustomExceptionHandler, log_info_message

logger = logging.getLogger("django")

@csrf_exempt
@swagger_auto_schema(
    method="post",
    request_body=TaskSerializer,
    responses={201: TaskSerializer},
    operation_id="Create Task"
)


@api_view(["POST"])
def create_task(request):
    logger.info(log_info_message(request, " create task"))
    response_obj = None
    try:
        serializer = TaskSerializer(request.data)
        if serializer.is_valid():
            task = serializer.save()
            response_obj = serializer.data
            return JsonResponse(response_obj)
        return JsonResponse(serializer.errors)
    except CustomExceptionHandler as e:
        logger.exception(f" Exception in create task: {e}")
        response_obj = get_response(eval(str(e)))
    except Exception as e:
        logger.exception(f"Exception in create task: {e}")
        response_obj = get_response("generic_error")
    return JsonResponse(response_obj, )

@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=TaskSerializer,
    responses={200: TaskSerializer},
    operation_id="Update Task"
)


@api_view(["PUT"])
def update_task(request):
    logger.info(log_info_message(request, f"Request to update task "))
    try:
        task = Task.objects.get(request.data)
        serializer = TaskSerializer(task, data=request.data, )
        if serializer.is_valid():
            task = serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    except Task.DoesNotExist:
        return JsonResponse({ "Task not found."})
    except Exception as e:
        logger.exception(f"Exception in update task: {e}")
        return JsonResponse(get_response("generic_error"))

@csrf_exempt
@swagger_auto_schema(
    method="post",
    operation_id="Assign Task"
)
@api_view(["POST"])
def assign_task(request, task_id, user_id):
    logger.info(log_info_message(request, f"Request to assign task {task_id} to user {user_id}"))
    try:
        task = Task.objects.get(id=task_id)
        task.user_id = user_id
        task.save()
        return JsonResponse({"message": "Task assigned successfully"})
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found."})
    except Exception as e:
        logger.exception(f"Exception in assign task: {e}")
        return JsonResponse(get_response("generic_error"))
    



@csrf_exempt
@swagger_auto_schema(
    method="get",
    operation_id="Get All Tasks"
)
@api_view(["GET"])
def get_tasks(request):
    logger.info(log_info_message(request, "Request to get all tasks"))
    try:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data)
    except Exception as e:
        logger.exception(f"Exception in get tasks: {e}")
        return JsonResponse(get_response("generic_error"))



@csrf_exempt
@swagger_auto_schema(
    method="get",
    operation_id="Search Tasks"
)
@api_view(["GET"])
def search_tasks(request):
    query = request.GET.get("query", "")
    logger.info(log_info_message(request, f"Request to search tasks with query: {query}"))
    try:
        tasks = Task.objects.filter(name__icontains=query)
        serializer = TaskSerializer(tasks)
        return JsonResponse(serializer.data)
    except Exception as e:
        logger.exception(f"Exception in search tasks: {e}")
        return JsonResponse(get_response("generic_error"))
    


