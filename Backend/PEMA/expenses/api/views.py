from decimal import Decimal

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView

from PEMA.utils.response_wrapper import custom_response
from .serializers import ExpenseSerializer
from ..models import Expense


class ExpenseCreateView(CreateAPIView):
    """
    API view to create a new Expense entry.
    Only authenticated users are permitted to create new Expense records.
    """
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    @extend_schema(
        summary="Create a New Expense",
        description="Allows authenticated users to create a new expense entry. Requires category ID and amount.",
        tags=["Expenses"],
        request=ExpenseSerializer,
        responses={
            201: OpenApiResponse(description="Expense created successfully.", response=ExpenseSerializer),
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Forbidden - Authentication required"),
        }
    )
    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new expense entry."""
        try:
            response = self.create(request, *args, **kwargs)
            return custom_response(
                status="success",
                message="Expense created successfully.",
                data=response.data,
                status_code=response.status_code,
            )
        except ValidationError as e:
            return custom_response(
                status="error",
                message="Validation error",
                data={"errors": e.detail},
                status_code=400,
            )
        except Exception as e:
            return custom_response(
                status="error",
                message="An unexpected error occurred.",
                data={"errors": str(e)},
                status_code=500,
            )

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
