from rest_framework.views import exception_handler

from .response_wrapper import custom_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Extract error details
        error_data = {}
        if hasattr(exc, "detail"):
            if isinstance(exc.detail, list):
                error_data = {"errors": exc.detail}
            elif isinstance(exc.detail, dict):
                error_data = {"errors": {key: value for key, value in exc.detail.items()}}
            else:
                error_data = {"errors": str(exc.detail)}

        return custom_response(
            status="error",
            message=error_data.get("errors", "An error occurred"),
            data=None,
            status_code=response.status_code,
        )

    # Default response for unhandled exceptions
    return custom_response(
        status="error",
        message="An unexpected error occurred",
        data=None,
        status_code=500,
    )
