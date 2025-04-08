def log_info_message(message):
    print(f"LOG: {message}")

def get_response(data, message="Success"):
    return {"data": data, "message": message}

def CustomExceptionHandler(exc, context):
    return {"error": str(exc)}

def generic_error_2():
    return {"error": "Something went wrong"}
