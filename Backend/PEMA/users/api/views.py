from djoser.views import UserViewSet as BaseUserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView,
    TokenVerifyView as BaseTokenVerifyView, TokenBlacklistView,
)

from PEMA.utils.response_wrapper import custom_response
from .serializers import UserProfileSerializer, RefreshTokenSerializer


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
        response = super().create(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="User successfully registered",
            data=response.data,
            status_code=response.status_code,
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
        response = super().activation(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="Account successfully activated",
            data=response.data,
            status_code=response.status_code,
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
        response = super().set_password(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="Password successfully updated",
            data=response.data,
            status_code=response.status_code,
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
        response = super().reset_password(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="Password reset email sent",
            data=response.data,
            status_code=response.status_code,
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
        response = super().reset_password_confirm(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="Password successfully reset",
            data=response.data,
            status_code=response.status_code,
        )


# Extending existing token views
class TokenObtainPairView(BaseTokenObtainPairView):
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
        response = super().post(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="Token successfully obtained",
            data=response.data,
            status_code=response.status_code,
        )


class TokenRefreshView(BaseTokenRefreshView):
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
        response = super().post(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="Access token successfully refreshed",
            data=response.data,
            status_code=response.status_code,
        )


class TokenVerifyView(BaseTokenVerifyView):
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
        response = super().post(request, *args, **kwargs)
        return custom_response(
            status="success",
            message="Token is valid",
            data=response.data,
            status_code=response.status_code,
        )


class TokenDestroyView(TokenBlacklistView):
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
