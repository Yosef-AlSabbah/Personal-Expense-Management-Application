from logging import getLogger

from djoser.views import UserViewSet as BaseUserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView,
    TokenVerifyView as BaseTokenVerifyView, TokenBlacklistView,
)

from PEMA.utils.response_wrapper import custom_response
from .serializers import UserProfileSerializer, RefreshTokenSerializer

logger = getLogger(__name__)


class UserViewSet(BaseUserViewSet):
    """
    View for managing user actions including profile operations and authentication flows.
    """

    @extend_schema(
        operation_id="user_me_retrieve",
        description="Retrieve the authenticated user's profile.",
        tags=["User Management"],
        methods=['GET'],
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="Invalid request."),
        }
    )
    @extend_schema(
        operation_id="user_me_update",
        description="Update the authenticated user's profile.",
        tags=["User Management"],
        methods=['PUT'],
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="Invalid request."),
        }
    )
    @extend_schema(
        operation_id="user_me_partial_update",
        description="Partially update the authenticated user's profile.",
        tags=["User Management"],
        methods=['PATCH'],
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="Invalid request."),
        }
    )
    @extend_schema(
        operation_id="user_me_delete",
        description="Delete the authenticated user's profile.",
        tags=["User Management"],
        methods=['DELETE'],
        responses={
            204: OpenApiResponse(description="No Content"),
            400: OpenApiResponse(description="Invalid request."),
        }
    )
    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def me(self, request, *args, **kwargs):
        """
        Manage operations on the authenticated user's profile.

        This method allows the user to perform the following actions on their profile:
        - GET: Retrieve the user's profile information.
        - PUT: Update the user's profile with the provided data.
        - PATCH: Partially update the user's profile with the provided fields.
        - DELETE: Remove the user's profile from the system.

        Depending on the HTTP method, the appropriate serializer and response will be used.
        """
        try:
            if request.method == "GET":
                serializer = self.get_serializer(request.user)
                return custom_response(
                    status="success", message="Profile retrieved", data=serializer.data
                )
            elif request.method in ["PUT", "PATCH"]:
                partial = request.method == "PATCH"
                serializer = self.get_serializer(
                    request.user, data=request.data, partial=partial
                )
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return custom_response(
                    status="success", message="Profile updated", data=serializer.data
                )
            elif request.method == "DELETE":
                user = request.user
                user.delete()
                return custom_response(
                    status="success",
                    message="Profile deleted",
                    data=None,
                    status_code=status.HTTP_204_NO_CONTENT,
                )
        except ValidationError as e:
            logger.error(f"Validation error during profile management: {e}")
            return custom_response(
                status="error", message="Validation error", data={"errors": e.detail}, status_code=400
            )
        except Exception as e:
            logger.error(f"Unexpected error during profile management: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
                status_code=500,
            )

    @extend_schema(
        operation_id="user_register",
        description="Register a new user account.",
        tags=["User Authentication"],
        methods=['POST'],
        responses={
            201: OpenApiResponse(
                description="User successfully registered. Please check your email to activate your account."),
            400: OpenApiResponse(description="Invalid request."),
            500: OpenApiResponse(description="An internal error occurred."),
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new user account.

        If the request is valid, it will return a 201 response with a success message.
        If the request is invalid, it will return a 400 response with an error message.
        """
        try:
            response = super().create(request, *args, **kwargs)

            return custom_response(
                status="success",
                message="User successfully registered. Please check your email to activate your account.",
                data=response.data,
                status_code=response.status_code,
            )
        except ValidationError as e:
            logger.error(f"Validation error during user registration: {e}")

            # Extract detailed error messages (only the message strings)
            detailed_errors = {}
            if hasattr(e, 'get_full_details'):
                for field, error_list in e.get_full_details().items():
                    detailed_errors[field] = [error['message'] for error in error_list]
            else:
                detailed_errors = str(e)

            return custom_response(
                status="error",
                message="Validation error occurred. Please check your input and try again.",
                data=None,
                errors=detailed_errors,
                status_code=400,
            )

        except Exception as e:
            logger.error(f"Unexpected error during user registration: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data=None,
                errors=None,  # Do not expose raw errors to the user
                status_code=500,
            )

    @extend_schema(
        operation_id="user_activate",
        description="Activate a user account using the activation key.",
        tags=["User Authentication"],
        methods=['POST'],
        responses={
            200: OpenApiResponse(description="Account successfully activated."),
            400: OpenApiResponse(description="Invalid activation key."),
        }
    )
    def activation(self, request, *args, **kwargs):
        """
        Activate a user account using the activation key.
        """
        try:
            response = super().activation(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Account successfully activated",
                data=response.data,
                status_code=response.status_code,
            )
        except ValidationError as e:
            logger.error(f"Activation error: {e}")
            return custom_response(
                status="error",
                message="Invalid activation key",
                errors=e.detail,  # Moved error details to errors field
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during account activation: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,  # Hide sensitive details
                status_code=500,
            )

    @extend_schema(
        operation_id="user_set_password",
        description="Set a new password for the authenticated user.",
        tags=["User Management"],
        methods=['POST'],
        responses={
            200: OpenApiResponse(description="Password successfully updated."),
            400: OpenApiResponse(description="Invalid password input."),
        }
    )
    def set_password(self, request, *args, **kwargs):
        """
        Set a new password for the authenticated user.
        """
        try:
            response = super().set_password(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Password successfully updated",
                data=response.data,
                status_code=response.status_code,
            )
        except ValidationError as e:
            logger.error(f"Validation error during password update: {e}")
            return custom_response(
                status="error",
                message="Invalid password input",
                errors=e.detail,  # Moved error details to errors field
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during password update: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,  # Hide sensitive details
                status_code=500,
            )

    @extend_schema(
        operation_id="user_reset_password",
        description="Initiate a password reset request.",
        tags=["User Management"],
        methods=['POST'],
        responses={
            200: OpenApiResponse(description="Password reset email sent."),
            400: OpenApiResponse(description="Invalid email address."),
        }
    )
    def reset_password(self, request, *args, **kwargs):
        """
        Initiate a password reset request.
        """
        try:
            response = super().reset_password(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Password reset email sent",
                data=response.data,
                status_code=response.status_code,
            )
        except ValidationError as e:
            logger.error(f"Validation error during password reset request: {e}")
            return custom_response(
                status="error",
                message="Invalid email address provided.",
                errors=e.detail,  # Moved error details to errors field
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during password reset request: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,  # Hide sensitive details
                status_code=500,
            )

    @extend_schema(
        operation_id="user_reset_password_confirm",
        description="Confirm a password reset using the token and new password.",
        tags=["User Management"],
        methods=['POST'],
        responses={
            200: OpenApiResponse(description="Password successfully reset."),
            400: OpenApiResponse(description="Invalid token or password."),
        }
    )
    def reset_password_confirm(self, request, *args, **kwargs):
        """
        Confirm a password reset using the token and new password.
        """
        try:
            response = super().reset_password_confirm(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Password successfully reset",
                data=response.data,
                status_code=response.status_code,
            )
        except ValidationError as e:
            logger.error(f"Validation error during password reset confirmation: {e}")
            return custom_response(
                status="error",
                message="Invalid token or password.",
                errors=e.detail,  # Moved error details to errors field
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during password reset confirmation: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,  # Hide sensitive details
                status_code=500,
            )


class TokenObtainPairView(BaseTokenObtainPairView):
    """
    Handle POST requests to obtain a new pair of access and refresh tokens.
    """

    @extend_schema(
        operation_id="token_obtain",
        description="Obtain a new pair of access and refresh tokens.",
        tags=["User Authentication"],
        responses={
            200: OpenApiResponse(description="Token successfully obtained."),
            400: OpenApiResponse(description="Invalid credentials."),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Token successfully obtained",
                data=response.data,
                status_code=response.status_code,
            )
        except AuthenticationFailed as e:
            logger.warning(f"Authentication failed: {e}")
            return custom_response(
                status="error",
                message="Invalid credentials",
                errors=None,  # Do not expose sensitive information
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during token obtain: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,
                status_code=500,
            )


class TokenRefreshView(BaseTokenRefreshView):
    """
    Handle POST requests to refresh an access token using a refresh token.
    """

    @extend_schema(
        operation_id="token_refresh",
        description="Refresh an access token using a refresh token.",
        tags=["User Authentication"],
        responses={
            200: OpenApiResponse(description="Access token successfully refreshed."),
            400: OpenApiResponse(description="Invalid refresh token."),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Access token successfully refreshed",
                data=response.data,
                status_code=response.status_code,
            )
        except InvalidToken as e:
            logger.warning(f"Invalid token error during token refresh: {e}")
            return custom_response(
                status="error",
                message="The provided token is invalid or expired.",
                errors=e.detail if hasattr(e, "detail") else {"detail": "Token not valid."},
                status_code=400,
            )
        except TokenError as e:
            logger.warning(f"Token error during token refresh: {e}")
            return custom_response(
                status="error",
                message="There was a problem with the token.",
                errors=e.detail if hasattr(e, "detail") else {"detail": "Token error."},
                status_code=400,
            )
        except ValidationError as e:
            logger.error(f"Validation error during token refresh: {e}")
            return custom_response(
                status="error",
                message="Invalid refresh token.",
                errors=e.detail,
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,
                status_code=500,
            )


class TokenVerifyView(BaseTokenVerifyView):
    """
    Verify if an access token is valid.
    """

    @extend_schema(
        operation_id="token_verify",
        description="Verify if an access token is valid.",
        tags=["User Authentication"],
        responses={
            200: OpenApiResponse(description="Token is valid."),
            401: OpenApiResponse(description="Token is invalid or expired."),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Token is valid",
                data=response.data,
                status_code=response.status_code,
            )
        except InvalidToken as e:
            logger.warning(f"Invalid token error during token verification: {e}")
            return custom_response(
                status="error",
                message="The provided token is invalid or expired.",
                errors=e.detail if hasattr(e, "detail") else {"detail": "Token not valid."},
                status_code=401,
            )
        except TokenError as e:
            logger.warning(f"Token error during token verification: {e}")
            return custom_response(
                status="error",
                message="There was a problem with the token.",
                errors=e.detail if hasattr(e, "detail") else {"detail": "Token error."},
                status_code=401,
            )
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,
                status_code=500,
            )


class TokenDestroyView(TokenBlacklistView):
    """
    Log out the user by blacklisting their refresh token.
    """
    serializer_class = RefreshTokenSerializer

    @extend_schema(
        operation_id="logout_user",
        description="Log out the user by blacklisting their refresh token.",
        tags=["User Authentication"],
        request=RefreshTokenSerializer,
        responses={
            205: OpenApiResponse(description="Successfully logged out"),
            400: OpenApiResponse(description="Invalid Token"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return custom_response(
                status="success",
                message="Successfully logged out",
                data=None,
                status_code=status.HTTP_205_RESET_CONTENT,
            )
        except InvalidToken as e:
            logger.warning(f"Invalid token error during logout: {e}")
            return custom_response(
                status="error",
                message="The provided token is invalid.",
                errors=e.detail if hasattr(e, "detail") else {"detail": "Token not valid."},
                status_code=400,
            )
        except TokenError as e:
            logger.warning(f"Token error during logout: {e}")
            return custom_response(
                status="error",
                message="There was a problem with the token.",
                errors=e.detail if hasattr(e, "detail") else {"detail": "Token error."},
                status_code=400,
            )
        except ValidationError as e:
            logger.error(f"Validation error during logout: {e}")
            return custom_response(
                status="error",
                message="Invalid token provided.",
                errors=e.detail,
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during logout: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,
                status_code=500,
            )
