from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView

from users.models import Profile
from .serializers import IncomeSerializer
from ..models import Income


class UpdateIncomeView(UpdateAPIView):
    """
    API view to update an existing Income entry for the authenticated user.
    """
    serializer_class = IncomeSerializer

    @extend_schema(
        summary="Update Income Entry",
        description="Update the authenticated user's income entry with the provided data.",
        tags=["Income"],
        request=IncomeSerializer,
        responses={
            200: OpenApiResponse(description="Income entry updated successfully.", response=IncomeSerializer),
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Forbidden - Authentication required"),
        }
    )
    def put(self, request, *args, **kwargs):
        """Handle PUT requests to update income data for the authenticated user."""
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial Update Income Entry",
        description="Partially update the authenticated user's income entry with the provided fields.",
        tags=["Income"],
        request=IncomeSerializer,
        responses={
            200: OpenApiResponse(description="Income entry partially updated successfully.", response=IncomeSerializer),
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Forbidden - Authentication required"),
        }
    )
    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests to partially update income data for the authenticated user."""
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        """Retrieve the Income object for the authenticated user, or raise an error if not found."""
        user = self.request.user
        try:
            return Income.objects.get(user=user)
        except Income.DoesNotExist:
            raise ValidationError("Income entry does not exist for this user.")

    def update(self, request, *args, **kwargs):
        """Override to check for changes in the income amount and update profile balance if needed."""
        instance = self.get_object()
        previous_amount = instance.amount
        response = super().update(request, *args, **kwargs)
        new_amount = response.data.get("amount")

        if new_amount != previous_amount:
            # Update the profile balance if income amount has changed
            profile = Profile.objects.get(user=request.user)
            profile.update_balance()

        return response
