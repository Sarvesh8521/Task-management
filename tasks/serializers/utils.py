import logging

logger = logging.getLogger("django")


def log_info_message(request, message):
    """Format a log message with request method and path."""
    return f"{request.method} {request.path} - {message}"


def get_response(message, status="error"):
    """Create a standardized response dict."""
    return {"status": status, "message": message}
