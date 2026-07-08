import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from tasks.models import Project
from tasks.serializers import ProjectSerializer

logger = logging.getLogger("django")


@swagger_auto_schema(
    method="post",
    request_body=ProjectSerializer,
    responses={201: ProjectSerializer},
    operation_id="Create Project",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_project(request):
    logger.info("POST %s - Create project", request.path)
    try:
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Exception in create project: %s", e)
        return JsonResponse({"error": "An error occurred while creating the project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="put",
    request_body=ProjectSerializer,
    responses={200: ProjectSerializer},
    operation_id="Update Project",
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_project(request, project_id):
    logger.info("PUT %s - Update project %d", request.path, project_id)
    try:
        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in update project: %s", e)
        return JsonResponse({"error": "An error occurred while updating the project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="delete",
    operation_id="Delete Project",
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id):
    logger.info("DELETE %s - Delete project %d", request.path, project_id)
    try:
        project = Project.objects.get(id=project_id)
        project.is_active = False
        project.save()
        return JsonResponse({"message": "Project deleted successfully."}, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Exception in delete project: %s", e)
        return JsonResponse({"error": "An error occurred while deleting the project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    operation_id="Get All Projects",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_projects(request):
    logger.info("GET %s - Get all projects", request.path)
    try:
        projects = Project.objects.filter(is_active=True)
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Exception in get all projects: %s", e)
        return JsonResponse({"error": "An error occurred while retrieving projects."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)