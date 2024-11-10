from decimal import Decimal

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView

from .serializers import ExpenseSerializer
from ..models import Expense


class ExpenseCreateView(CreateAPIView):
    """
    API view to create a new Expense entry.
    Only authenticated users are permitted to create new Expense records.
    """
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

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
        """Assign the authenticated user as the owner of the expense entry upon creation,
        and ensure the user's balance can cover the expense.
        """
        user = self.request.user
        profile = user.profile  # Access the user's profile for balance checking
        amount = serializer.validated_data['amount']

        # Check if the user's balance can cover the expense amount
        if profile.balance < amount:
            raise ValidationError("Insufficient balance to cover this expense.")

        # Deduct the expense from balance and save the profile
        profile.balance -= Decimal(amount)
        profile.save()

        # Save the expense with the associated user
        serializer.save(user=user)
