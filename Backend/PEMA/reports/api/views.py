from datetime import date
from decimal import Decimal
from logging import getLogger

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView

from PEMA.utils.response_wrapper import custom_response
from expenses.api.serializers import ExpenseSerializer
from expenses.models import Expense
from reports.api.serializers import MonthlyStatisticsSerializer
from users.models import Profile

# Configure logging for detailed error tracking
logger = getLogger(__name__)


@extend_schema(
    summary="List Monthly Expenses",
    description="Retrieve a list of expenses for the current month.",
    tags=["Reports"],
    responses={
        200: OpenApiResponse(
            description="A list of expenses for the current month",
            response=ExpenseSerializer(many=True)
        ),
        403: OpenApiResponse(description="Forbidden - Authentication required"),
        500: OpenApiResponse(description="Internal server error"),
    }
)
class ExpenseReportView(ListAPIView):
    """API view to retrieve a list of expenses for the current month."""
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.none()

    def get_queryset(self):
        """Retrieve expenses for the authenticated user within the current month."""
        try:
            return Expense.objects.get_expenses_for_current_month(user=self.request.user)
        except ObjectDoesNotExist:
            raise ValidationError("No expenses found for the current month.")
        except Exception as e:
            logger.error(f"Unexpected error in get_queryset: {e}", exc_info=True)
            raise e

    def list(self, request, *args, **kwargs):
        """Custom response for the list of expenses."""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return custom_response(
                status="success",
                message="Monthly expenses retrieved successfully",
                data=serializer.data
            )
        except ValidationError as e:
            return custom_response(
                status="error",
                message="Validation error.",
                errors=e.detail,
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Unexpected error in list: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                status_code=500,
            )


@extend_schema(
    summary="List Categorized Monthly Expenses",
    description="Retrieve categorized expenses for the current month.",
    tags=["Reports"],
    responses={
        200: OpenApiResponse(
            description="A dictionary of expenses categorized by type for the current month",
            response=OpenApiTypes.OBJECT
        ),
        403: OpenApiResponse(description="Forbidden - Authentication required"),
        500: OpenApiResponse(description="Internal server error"),
    }
)
class ExpenseCategoryReportView(ListAPIView):
    """API view to retrieve categorized expenses for the current month."""
    serializer_class = ExpenseSerializer

    def list(self, request, *args, **kwargs):
        """Return expenses grouped by category for the current month."""
        try:
            expenses_by_category = request.user.expenses.get_expenses_by_category_for_current_month(
                user=self.request.user)
            data = {str(category): ExpenseSerializer(expenses, many=True).data
                    for category, expenses in expenses_by_category.items()}
            return custom_response(
                status="success",
                message="Categorized monthly expenses retrieved successfully",
                data=data
            )
        except AttributeError as e:
            logger.error(f"Invalid attribute: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="Unable to retrieve categorized expenses. Please try again later.",
                status_code=500,
            )
        except Exception as e:
            logger.error(f"Unexpected error in list: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                status_code=500,
            )


class MonthlyStatisticsView(APIView):
    """
    API view to provide monthly statistics for the authenticated user.
    Returns total expenses, remaining balance, and average daily expenditure.
    """

    @extend_schema(
        summary="Monthly Financial Statistics",
        description="Retrieve monthly statistics including total expenses, remaining balance, and average daily expenditure.",
        tags=["Reports"],
        responses={
            200: OpenApiResponse(
                description="Monthly financial statistics",
                response=MonthlyStatisticsSerializer
            ),
            403: OpenApiResponse(description="Forbidden - Authentication required"),
            500: OpenApiResponse(description="Internal server error"),
        }
    )
    def get(self, request, *args, **kwargs):
        """Retrieve financial statistics in a flat response structure."""
        try:
            profile = get_object_or_404(Profile, user=request.user)
            total_expenses = Expense.objects.filter(
                user=request.user, date__month=date.today().month
            ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            remaining_balance = profile.balance - total_expenses
            average_daily_expense = total_expenses / max(1, date.today().day)

            stats = {
                "total_expenses": total_expenses,
                "remaining_balance": remaining_balance,
                "average_daily_expense": average_daily_expense,
            }
            serializer = MonthlyStatisticsSerializer(stats)
            return custom_response(
                status="success",
                message="Monthly statistics retrieved successfully",
                data=serializer.data
            )
        except Exception as e:
            logger.error(f"Unexpected error in get: {e}", exc_info=True)
            return custom_response(
                status="error",
                message="An unexpected error occurred. Please try again later.",
                status_code=500,
            )
