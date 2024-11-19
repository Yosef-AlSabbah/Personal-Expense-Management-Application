from rest_framework.response import Response


def custom_response(status, data=None, message=None, errors=None, status_code=200):
    """
    Utility to standardize API responses.
    """
    return Response(
        {
            "status": status,  # success or error
            "data": data,
            "message": message,
            "errors": errors,
        },
        status=status_code,
    )
