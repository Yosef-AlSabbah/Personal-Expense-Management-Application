from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from expenses.api.serializers import ExpenseSerializer
from expenses.models import Expense
from reports.api.serializers import MonthlyStatisticsSerializer
from users.models import Profile


@extend_schema(
    summary="List Monthly Expenses",
    description="Retrieve a list of expenses for the current month.",
    tags=["Reports"],
    responses={
        200: OpenApiResponse(
            description="A list of expenses for the current month",
            response=ExpenseSerializer(many=True)
        ),
        403: OpenApiResponse(description="Forbidden - Authentication required")
    }
)
class ExpenseReportView(ListAPIView):
    """API view to retrieve a list of expenses for the current month."""
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        """Retrieve expenses for the authenticated user within the current month."""
        return Expense.objects.get_expenses_for_current_month(user=self.request.user)


@extend_schema(
    summary="List Categorized Monthly Expenses",
    description="Retrieve categorized expenses for the current month.",
    tags=["Reports"],
    responses={
        200: OpenApiResponse(
            description="A dictionary of expenses categorized by type for the current month",
            response=OpenApiTypes.OBJECT  # Updated to use OpenApiTypes for flexibility
        ),
        403: OpenApiResponse(description="Forbidden - Authentication required")
    }
)
class ExpenseCategoryReportView(ListAPIView):
    """API view to retrieve categorized expenses for the current month."""
    serializer_class = ExpenseSerializer

    def list(self, request, *args, **kwargs):
        """Return expenses grouped by category for the current month."""
        expenses_by_category = request.user.expenses.get_expenses_by_category_for_current_month()
        data = {str(category): ExpenseSerializer(expenses, many=True).data
                for category, expenses in expenses_by_category.items()}
        return Response(data)


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
            403: OpenApiResponse(description="Forbidden - Authentication required")
        }
    )
    def get(self, request, *args, **kwargs):
        """Retrieve financial statistics for the authenticated user's current month."""
        profile = get_object_or_404(Profile, user=request.user)
        stats = Profile.objects.current_month_statistics(user=request.user)
        serializer = MonthlyStatisticsSerializer(stats)
        return Response(serializer.data, status=HTTP_200_OK)
