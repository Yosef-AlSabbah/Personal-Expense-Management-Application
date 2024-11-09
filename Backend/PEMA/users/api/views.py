from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserProfileUpdateSerializer
from ..models import Profile

User = get_user_model()


class UserProfileUpdateView(UpdateAPIView):
    """
    API view to update the profile information of the authenticated user.
    Allows updating the user's details and profile picture.
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Updates the authenticated user's profile with full data (PUT) or partial data (PATCH).",
        operation_summary="Update User Profile",
        tags=["User Profile"],
        request_body=UserProfileUpdateSerializer,
        responses={
            200: UserProfileUpdateSerializer,
            400: openapi.Response("Validation Error"),
            403: openapi.Response("Forbidden - Authentication required"),
            500: openapi.Response("Server error")
        }
    )
    def put(self, request, *args, **kwargs):
        """Handle PUT requests to update full profile data."""
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially updates the authenticated user's profile with provided fields only.",
        operation_summary="Partial Update User Profile",
        tags=["User Profile"],
        request_body=UserProfileUpdateSerializer,
        responses={
            200: UserProfileUpdateSerializer,
            400: openapi.Response("Validation Error"),
            403: openapi.Response("Forbidden - Authentication required"),
            500: openapi.Response("Server error")
        }
    )
    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests to partially update profile data."""
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        """Retrieve the profile instance associated with the authenticated user."""
        return self.request.user.profile

    def perform_update(self, serializer):
        """Save the updated profile data and handle validation errors."""
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError({"detail": "Failed to update profile. Error: " + str(e)})
