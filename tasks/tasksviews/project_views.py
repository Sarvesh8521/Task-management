from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
import logging

from tasks.models import Project
from tasks.serializers import ProjectSerializer
from tasks.serializers import get_response, CustomExceptionHandler, log_info_message, generic_error_2


logger = logging.getLogger("django")

@csrf_exempt
@swagger_auto_schema(
    method="post",
    request_body=ProjectSerializer,
    responses={201: ProjectSerializer},
    operation_id="Create Project"
)
@api_view(["POST"])
def create_project(request):
    logger.info(log_info_message(request, "Request to create project"))
    response_obj = None

    try:
        serializer = ProjectSerializer(request.data)
        if serializer.is_valid():
            project = serializer.save()
            response_obj = serializer.data
            return JsonResponse(response_obj)
        else:
            return JsonResponse(serializer.errors)

    except CustomExceptionHandler as e:
        logger.exception(f" Exception in create project: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in create project: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in create project %s", response_obj)
    return JsonResponse(response_obj)


@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=ProjectSerializer,
    responses={200: ProjectSerializer},
    operation_id="Update Project"
)
@api_view(["PUT"])
def update_project(request):
    logger.info(log_info_message(request, "Request to update project with ID: %s"))
    response_obj = None

    try:
        project = Project.objects.get(request.data)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    except Project.DoesNotExist:
        response_obj = { "Project not found."}
        return JsonResponse(response_obj)

    except CustomExceptionHandler as e:
        logger.exception(f" Exception in update project: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in update project: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in update project  %s", response_obj)
    return JsonResponse(response_obj)