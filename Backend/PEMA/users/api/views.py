from logging import getLogger

from djoser.views import UserViewSet as BaseUserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
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
            201: OpenApiResponse(description="User successfully registered."),
            400: OpenApiResponse(description="Invalid request."),
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
                message="User successfully registered",
                data=response.data,
                status_code=response.status_code,
            )
        except ValidationError as e:
            logger.error(f"Validation error during user registration: {e}")
            return custom_response(
                status="error", message="Validation error", data={"errors": e.detail}, status_code=400
            )
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
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
        """Activate a user account using the activation key."""
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
                status="error", message="Invalid activation key", data={"errors": e.detail}, status_code=400
            )
        except Exception as e:
            logger.error(f"Unexpected error during account activation: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
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

        If the new password is valid, it will return a 200 response with a success message.
        If the new password is invalid, it will return a 400 response with an error message.
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
                status="error", message="Invalid password input", data={"errors": e.detail}, status_code=400
            )
        except Exception as e:
            logger.error(f"Unexpected error during password update: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
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

        If the email is valid, it will return a 200 response with a success message.
        If the email is invalid, it will return a 400 response with an error message.
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
                data={"errors": e.detail},
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during password reset request: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
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

        If the token and password are valid, it will return a 200 response with a success message.
        If the token or password are invalid, it will return a 400 response with an error message.
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
                data={"errors": e.detail},
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error during password reset confirmation: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
                status_code=500,
            )


# Extending existing token views
class TokenObtainPairView(BaseTokenObtainPairView):
    """
    Handle POST requests to obtain a new pair of access and refresh tokens.

    This method overrides the default POST behavior to provide a custom response
    when a user successfully obtains tokens. The response includes a success message
    and the token data. If the credentials are invalid, an error response is returned.
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
                status="error", message="Invalid credentials", data={}, status_code=400
            )
        except Exception as e:
            logger.error(f"Unexpected error during token obtain: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
                status_code=500,
            )


class TokenRefreshView(BaseTokenRefreshView):
    """
    Handle POST requests to refresh an access token using a refresh token.

    This endpoint is used to refresh an access token using a refresh token.
    The request should contain a valid refresh token in the request body.
    If the token is valid, it will return a 200 response with a new access token.
    If the token is invalid or expired, it will return a 400 response with an error message.
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
        except ValidationError as e:
            logger.error(f"Validation error during token refresh: {e}")
            return custom_response(
                status="error", message="Invalid refresh token", data={"errors": e.detail}, status_code=400
            )
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
                status_code=500,
            )


class TokenVerifyView(BaseTokenVerifyView):
    """
    Verify if an access token is valid.

    This endpoint is used to verify if an access token is valid or not.
    If the token is valid, it will return a 200 response with a success message.
    If the token is invalid or expired, it will return a 401 response with an error message.
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
        except ValidationError as e:
            logger.warning(f"Validation error during token verification: {e}")
            return custom_response(
                status="error", message="Token is invalid or expired", data={"errors": e.detail}, status_code=401
            )
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
                status_code=500,
            )


class TokenDestroyView(TokenBlacklistView):
    """
    Log out the user by blacklisting their refresh token.

    This endpoint is used to log out the user by blacklisting their refresh token.
    The request should contain a valid refresh token in the request body.
    If the token is valid, it will return a 200 response with a success message.
    If the token is invalid or expired, it will return a 400 response with an error message.
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
                {
                    "status": "success",
                    "message": "Successfully logged out",
                    "data": None
                },
                status_code=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return custom_response(
                {
                    "status": "error",
                    "message": "Validation error",
                    "data": {"errors": e.detail},
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return custom_response(
                {
                    "status": "error",
                    "message": "Invalid token or request format",
                    "data": None,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
