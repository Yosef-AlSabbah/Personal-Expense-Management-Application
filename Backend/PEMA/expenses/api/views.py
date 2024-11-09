from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ExpenseSerializer
from ..models import Expense


class ExpenseCreateView(CreateAPIView):
    """
    API view to create a new Expense entry.
    Only authenticated users are permitted to create new Expense records.
    """
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a New Expense",
        operation_description="Allows authenticated users to create a new expense entry. Requires category ID and amount.",
        tags=["Expenses"],
        request_body=ExpenseSerializer,
        responses={
            201: openapi.Response("Expense created successfully.", ExpenseSerializer),
            400: openapi.Response("Validation error"),
            403: openapi.Response("Forbidden - Authentication required"),
        }
    )
    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new expense entry."""
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Assign the authenticated user as the owner of the expense entry upon creation."""
        serializer.save(user=self.request.user)
