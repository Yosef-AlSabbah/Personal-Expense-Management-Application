from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_summary="Update Income Entry",
        operation_description="Update the authenticated user's income entry with the provided data.",
        tags=["Income"],
        request_body=IncomeSerializer,
        responses={
            200: openapi.Response("Income entry updated successfully.", IncomeSerializer),
            400: openapi.Response("Validation error"),
            403: openapi.Response("Forbidden - Authentication required"),
        }
    )
    def put(self, request, *args, **kwargs):
        """Handle PUT requests to update income data for the authenticated user."""
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Income Entry",
        operation_description="Partially update the authenticated user's income entry with the provided fields.",
        tags=["Income"],
        request_body=IncomeSerializer,
        responses={
            200: openapi.Response("Income entry partially updated successfully.", IncomeSerializer),
            400: openapi.Response("Validation error"),
            403: openapi.Response("Forbidden - Authentication required"),
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
