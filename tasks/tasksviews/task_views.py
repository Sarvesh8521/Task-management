import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from tasks.serializers.taskserializers import TaskSerializer
from tasks.models import Task

logger = logging.getLogger("django")


@swagger_auto_schema(
    method="post",
    request_body=TaskSerializer,
    responses={201: TaskSerializer},
    operation_id="Create Task",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    logger.info("POST %s - Create task", request.path)
    try:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Exception in create task: %s", e)
        return JsonResponse({"error": "An error occurred while creating the task."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="put",
    request_body=TaskSerializer,
    responses={200: TaskSerializer},
    operation_id="Update Task",
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    logger.info("PUT %s - Update task %d", request.path, task_id)
    try:
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in update task: %s", e)
        return JsonResponse({"error": "An error occurred while updating the task."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="post",
    operation_id="Assign Task",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_task(request, task_id, user_id):
    logger.info("POST %s - Assign task %d to user %d", request.path, task_id, user_id)
    try:
        task = Task.objects.get(id=task_id)
        task.users = user_id
        task.save()
        return JsonResponse({"message": "Task assigned successfully."}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in assign task: %s", e)
        return JsonResponse({"error": "An error occurred while assigning the task."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    operation_id="Get All Tasks",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    logger.info("GET %s - Get all tasks", request.path)
    try:
        tasks = Task.objects.filter(is_active=True)
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Exception in get tasks: %s", e)
        return JsonResponse({"error": "An error occurred while retrieving tasks."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    operation_id="Search Tasks",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_tasks(request):
    query = request.GET.get("query", "")
    logger.info("GET %s - Search tasks: %s", request.path, query)
    try:
        tasks = Task.objects.filter(name__icontains=query, is_active=True)
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Exception in search tasks: %s", e)
        return JsonResponse({"error": "An error occurred while searching tasks."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="delete",
    operation_id="Delete Task",
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    logger.info("DELETE %s - Delete task %d", request.path, task_id)
    try:
        task = Task.objects.get(id=task_id)
        task.is_active = False
        task.save()
        return JsonResponse({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in delete task: %s", e)
        return JsonResponse({"error": "An error occurred while deleting the task."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)