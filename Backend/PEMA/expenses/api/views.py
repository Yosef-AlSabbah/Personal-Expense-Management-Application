from decimal import Decimal, InvalidOperation
from logging import getLogger

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from rest_framework.generics import CreateAPIView

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
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return custom_response(
                status="error",
                message="Validation error occurred. Please check your input.",
                errors=e.detail,  # Use errors field for validation issues
                status_code=400,
            )
        except (AuthenticationFailed, PermissionDenied) as e:
            logger.warning(f"Authentication or permission error: {e}")
            return custom_response(
                status="error",
                message="You do not have permission to perform this action.",
                errors=None,  # No sensitive details exposed
                status_code=403,
            )
        except (IntegrityError, ObjectDoesNotExist, InvalidOperation) as e:
            logger.error(f"System error: {e}")  # Log the detailed error for debugging
            return custom_response(
                status="error",
                message="A system error occurred. Please contact support.",
                errors=None,  # Hide implementation details
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)  # Log stack trace for debugging
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                errors=None,  # Hide unhandled exception details
                status_code=500,
            )

    def perform_create(self, serializer):
        """
        Assign the authenticated user as the owner of the expense entry,
        and ensure the user's balance can cover the expense.
        """
        user = self.request.user
        profile = getattr(user, 'profile', None)  # Safely access profile

        if not profile:
            logger.error("User profile is missing or incomplete.")
            raise ValidationError("User profile is missing or incomplete.")

        amount = serializer.validated_data.get('amount', Decimal(0))

        if not isinstance(amount, Decimal):
            logger.error(f"Invalid amount type: {amount}")
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
