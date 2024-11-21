from decimal import Decimal, InvalidOperation
from logging import getLogger

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from PEMA.utils.response_wrapper import custom_response
from .serializers import ExpenseSerializer
from ..models import Expense

# Configure logging for detailed error tracking
logger = getLogger(__name__)


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
            500: OpenApiResponse(description="Internal server error"),
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
        except (ValidationError, AuthenticationFailed, PermissionDenied) as e:
            # Safe to show user-friendly validation/authentication errors
            return custom_response(
                status="error",
                message=str(e),
                data={},
                status_code=400 if isinstance(e, ValidationError) else 403,
            )
        except (IntegrityError, ObjectDoesNotExist, InvalidOperation) as e:
            logger.error(f"Handled exception: {e}")  # Log the detailed error for debugging
            return custom_response(
                status="error",
                message="A system error occurred. Please contact support.",
                data={},
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)  # Log stack trace for unhandled exceptions
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data={},
                status_code=500,
            )

    def perform_create(self, serializer):
        """Assign the authenticated user as the owner of the expense entry,
        and ensure the user's balance can cover the expense."""
        user = self.request.user
        profile = getattr(user, 'profile', None)  # Safely access profile

        if not profile:
            raise ValidationError("User profile is missing or incomplete.")

        amount = serializer.validated_data.get('amount', Decimal(0))

        if not isinstance(amount, Decimal):
            raise ValidationError("The amount must be a valid decimal number.")

        # Validate the user's balance
        if profile.balance < amount:
            logger.error(f"Insufficient balance: {profile.balance} < {amount}")
            raise ValidationError("Insufficient balance to cover this expense.")

        # Deduct the expense amount from the balance
        profile.balance -= amount
        profile.save()

        # Save the expense record
        serializer.save(user=user)
