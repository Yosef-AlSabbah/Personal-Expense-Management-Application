from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserProfileSerializer, RefreshTokenSerializer
from ..permissions import IsOwnerOrAdmin


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


class UserCreateView(CreateAPIView):
    """
    View for creating a new user and their profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = []  # No authentication required to create a new user

    @extend_schema(
        operation_id="register_user",
        description="Register a new user with their profile.",
        tags=["User Registration"],
        responses={
            201: UserProfileSerializer,
            400: OpenApiResponse(description="Validation Error"),
        },
    )
    def post(self, request, *args, **kwargs):
        # Handle POST request to create a new user and their profile
        return super().post(request, *args, **kwargs)


class TokenDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenSerializer  # Set the serializer here

    @extend_schema(
        operation_id="logout_user",
        description="Log out the user by blacklisting their refresh token.",
        tags=["User Authentication"],
        responses={
            205: OpenApiResponse(description="Successfully logged out"),
            400: OpenApiResponse(description="Invalid Token"),
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            # Validate the request data using the serializer
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to log the user out
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # Return error response if token is invalid or other issues occur
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
