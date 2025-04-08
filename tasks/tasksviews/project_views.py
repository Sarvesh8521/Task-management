from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
import logging

from tasks.models import Project
from tasks.serializers import ProjectSerializer
from tasks.serializers.utils import log_info_message, get_response, CustomExceptionHandler, generic_error_2


logger = logging.getLogger("django")


# class CustomExceptionHandler(Exception):
#     """Custom exception placeholder."""
#     pass

# def log_info_message(request, message):
#     """Formats a basic log message."""
#     return f"{request.method} {request.get_full_path()} - {message}"

# def get_response(error_key):
#     """Returns a basic error response."""
#     responses = {
#         "generic_error": {"error": "Something went wrong."},
#         "generic_error_2": {"error": "Unexpected error occurred."}
#     }
#     return responses.get(error_key, {"error": "Unknown error occurred."})

# generic_error_2 = "generic_error_2"




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
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            response_obj = serializer.data
            return JsonResponse(response_obj, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    except CustomExceptionHandler as e:
        logger.exception(f"Exception in create project: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in create project: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in create project %s", response_obj)
    return JsonResponse(response_obj, status=500)


@csrf_exempt
@swagger_auto_schema(
    method="put",
    request_body=ProjectSerializer,
    responses={200: ProjectSerializer},
    operation_id="Update Project"
)
@api_view(["PUT"])
def update_project(request):
    logger.info(log_info_message(request, "Request to update project"))
    response_obj = None

    try:
        project_id = request.data.get("id")
        if not project_id:
            return JsonResponse({"error": "Project ID is required."}, status=400)

        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    except Project.DoesNotExist:
        response_obj = {"error": "Project not found."}
        return JsonResponse(response_obj, status=404)

    except CustomExceptionHandler as e:
        logger.exception(f"Exception in update project: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in update project: {e}")
        response_obj = get_response(generic_error_2)

    logger.info("Response in update project %s", response_obj)
    return JsonResponse(response_obj, status=500)
