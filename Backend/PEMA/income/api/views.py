# income/views.py

from decimal import Decimal
from logging import getLogger

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from PEMA.utils.response_wrapper import custom_response
from users.models import Profile
from .serializers import IncomeSerializer
from ..models import Income

logger = getLogger(__name__)


class UpdateIncomeView(UpdateAPIView):
    """API view to update an existing Income entry for the authenticated user."""
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update Income Entry",
        description="Update the authenticated user's income entry with the provided data.",
        tags=["Income"],
        request=IncomeSerializer,
        responses={
            200: OpenApiResponse(description="Income entry updated successfully.", response=IncomeSerializer),
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Forbidden - Authentication required"),
            404: OpenApiResponse(description="Income entry not found"),
            500: OpenApiResponse(description="Internal server error"),
        }
    )
    def put(self, request, *args, **kwargs):
        """Handle PUT requests to update income data for the authenticated user."""
        return self._handle_request(self.update, request, *args, **kwargs)

    @extend_schema(
        summary="Partial Update Income Entry",
        description="Partially update the authenticated user's income entry with the provided fields.",
        tags=["Income"],
        request=IncomeSerializer,
        responses={
            200: OpenApiResponse(description="Income entry partially updated successfully.", response=IncomeSerializer),
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Forbidden - Authentication required"),
            404: OpenApiResponse(description="Income entry not found"),
            500: OpenApiResponse(description="Internal server error"),
        }
    )
    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests to partially update income data for the authenticated user."""
        return self._handle_request(self.partial_update, request, *args, **kwargs)

    def get_object(self):
        """Retrieve the Income object for the authenticated user, or raise an error if not found."""
        user = self.request.user
        try:
            return Income.objects.get(user=user)
        except Income.DoesNotExist as e:
            logger.warning(f"Income entry not found for user {user.id}: {e}")
            raise ValidationError(
                detail={"error": "Income entry does not exist for this user."},
                code="income_not_found"
            )

    def update(self, request, *args, **kwargs):
        """Override to check for changes in the income amount and update profile balance if needed."""
        try:
            instance = self.get_object()
            previous_amount = instance.amount
            response = super().update(request, *args, **kwargs)
            new_amount = Decimal(response.data.get("amount", "0.00"))

            if new_amount != previous_amount:
                # Update the profile balance with the difference
                self._update_profile_balance(request.user, previous_amount, new_amount)

            return custom_response(
                status="success",
                message="Income entry updated and profile balance adjusted.",
                data=response.data,
                status_code=response.status_code,
            )
        except Profile.DoesNotExist:
            logger.error(f"Profile not found for user {request.user.id}.")
            raise ValidationError({"error": "User profile does not exist."})
        except Exception as e:
            logger.error(f"Unexpected error during update: {e}", exc_info=True)
            raise e

    def _handle_request(self, method, request, *args, **kwargs):
        """Handle request with improved exception handling specific to this view."""
        try:
            response = method(request, *args, **kwargs)
            return Response(response.data)
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return custom_response(
                status="error",
                message="Validation error.",
                data=None,  # Ensure no data is returned
                errors=e.detail,
                status_code=400,
            )
        except AuthenticationFailed as e:
            logger.warning(f"Authentication error: {e}")
            return custom_response(
                status="error",
                message="Authentication required.",
                data=None,  # Ensure data is None
                errors={"detail": str(e)},  # Populate the errors field with the detail message
                status_code=401,
            )
        except PermissionDenied as e:
            logger.warning(f"Permission error: {e}")
            return custom_response(
                status="error",
                message="Permission denied.",
                data=None,  # Ensure no data is returned
                errors={"detail": str(e)},  # Extract error details
                status_code=403,
            )
        except ObjectDoesNotExist as e:
            logger.error(f"Object does not exist: {e}")
            return custom_response(
                status="error",
                message="Income entry does not exist.",
                data=None,  # Ensure no data is returned
                errors={"error": str(e)},
                status_code=404,
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="A database error occurred. Please contact support.",
                data=None,  # Ensure no data is returned
                errors={"database": "Integrity error."},
                status_code=500,
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                data=None,  # Ensure no data is returned
                errors={"unexpected": "An unexpected error occurred."},
                status_code=500,
            )

    def _update_profile_balance(self, user, previous_amount, new_amount):
        """Update the profile balance for the given user based on income change."""
        try:
            profile = Profile.objects.get(user=user)
            difference = new_amount - previous_amount
            profile.balance += difference
            profile.save()
            logger.debug(f"Updated balance for user {user.id}: {profile.balance} (Difference: {difference})")
        except Profile.DoesNotExist as e:
            logger.error(f"Profile not found for user {user.id}: {e}")
            raise ValidationError({"error": "User profile does not exist."})
