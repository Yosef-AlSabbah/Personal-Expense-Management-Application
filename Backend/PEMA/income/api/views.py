from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import IncomeSerializer
from ..models import Income


class CreateOrUpdateIncomeView(RetrieveUpdateAPIView):
    """
    API view to create or update an Income entry for the authenticated user.
    If an Income entry exists, it will be updated; otherwise, a new entry will be created.
    """
    serializer_class = IncomeSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve or Create Income Entry",
        operation_description="Retrieve the authenticated user's income entry. If it doesn't exist, create a new entry.",
        tags=["Income"],
        responses={
            200: IncomeSerializer,
            201: openapi.Response("Income entry created successfully.", IncomeSerializer),
            403: openapi.Response("Forbidden - Authentication required")
        }
    )
    def get(self, request, *args, **kwargs):
        """Retrieve or create the income entry for the authenticated user."""
        return self.retrieve(request, *args, **kwargs)

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
        """Retrieve or create the Income object for the authenticated user."""
        user = self.request.user
        income, created = Income.objects.get_or_create(user=user)
        return income
