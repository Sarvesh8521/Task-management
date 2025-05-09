from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
import logging

from tasks.models import Project
from tasks.serializers import ProjectSerializer

from tasks.serializers.utils import log_info_message


logger = logging.getLogger("django")


@csrf_exempt
@swagger_auto_schema(
    method="post",
    request_body=ProjectSerializer,
    responses={201: ProjectSerializer},
    operation_id="Create Project")


@api_view(["POST"])
def create_project(request):
    try:
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        logger.exception(f"Project creation failed: {str(e)}")
        return JsonResponse({"error": "Project creation failed."}, status=500)



@api_view(["PUT"])
def update_project(request, project_id):
    logger.info("Request to update project")
    try:
        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found."}, status=404)
    except Exception as e:
        logger.exception(f"Exception in update project: {e}")
        return JsonResponse("generic_error")
    

@api_view(["DELETE"])
def delete_project(request, project_id):    
    logger.info("Request to delete project")
    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        return JsonResponse({"message": "Project deleted"})
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"})
    except Exception as e:
        logger.exception(f"Exception in delete project: {e}")
        return JsonResponse({"error": "An error occurred while deleting project"})
    



@api_view(["GET"])
def get_all_projects(request):    
    logger.info("Request to get all projects")
    try:
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        logger.exception(f"Exception in get all projects: {e}")
        return JsonResponse({"error": "An error occurred while getting all projects"})