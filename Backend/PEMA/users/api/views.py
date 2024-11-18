from djoser.views import UserViewSet as BaseUserViewSet
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView,
    TokenVerifyView as BaseTokenVerifyView,
)

from .serializers import UserProfileSerializer, RefreshTokenSerializer
from ..permissions import IsOwnerOrAdmin


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
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(request.user, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            user = request.user
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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
        return super().create(request, *args, **kwargs)

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
        return super().activation(request, *args, **kwargs)

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
        return super().set_password(request, *args, **kwargs)

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
        return super().reset_password(request, *args, **kwargs)

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
        return super().reset_password_confirm(request, *args, **kwargs)


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
        return super().post(request, *args, **kwargs)


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
        return super().post(request, *args, **kwargs)


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
        return super().post(request, *args, **kwargs)


class CurrentUserProfileView(RetrieveUpdateAPIView):
    """
    View for retrieving or updating the current user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    @extend_schema(
        operation_id="retrieve_or_update_profile",
        description="Retrieve or update the authenticated user's profile.",
        tags=["User Profile"],
        responses={
            200: UserProfileSerializer,
            403: OpenApiResponse(description="Permission Denied"),
        },
    )
    def get(self, request, *args, **kwargs):
        # Handle GET request to retrieve the user's profile information
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_profile",
        description="Update the authenticated user's profile.",
        tags=["User Profile"],
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="Validation Error"),
            403: OpenApiResponse(description="Permission Denied"),
        },
    )
    def patch(self, request, *args, **kwargs):
        # Handle PATCH request to update the user's profile information
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        # Return the profile of the authenticated user
        return self.request.user.profile


class TokenDestroyView(APIView):
    """
    Custom view to handle token destruction (logout).
    """

    @extend_schema(
        operation_id="logout_user",
        description="Log out the user by blacklisting their refresh token.",
        tags=["User Authentication"],
        request=RefreshTokenSerializer,  # Explicitly specify the request schema
        responses={
            205: OpenApiResponse(description="Successfully logged out"),
            400: OpenApiResponse(description="Invalid Token"),
        },
    )
    def post(self, request, *args, **kwargs):  # Using POST explicitly
        serializer = RefreshTokenSerializer(data=request.data)  # Use serializer directly
        try:
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Invalid token or request format"},
                status=status.HTTP_400_BAD_REQUEST,
            )
