from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from expenses.api.serializers import ExpenseSerializer
from expenses.models import Expense
from reports.api.serializers import MonthlyStatisticsSerializer
from users.models import Profile


class ExpenseReportView(ListAPIView):
    """
    API view to retrieve a list of expenses for the current month.
    Allows authenticated users to view their own expenses within the current month.
    """
    serializer_class = ExpenseSerializer

    @swagger_auto_schema(
        operation_summary="List Monthly Expenses",
        operation_description="Retrieve a list of expenses for the current month.",
        tags=["Expenses"],
        responses={
            200: openapi.Response(
                description="A list of expenses for the current month",
                schema=ExpenseSerializer(many=True)
            ),
            403: openapi.Response("Forbidden - Authentication required")
        }
    )
    def get_queryset(self):
        """Retrieve expenses for the authenticated user within the current month."""
        return Expense.objects.get_expenses_for_current_month(user=self.request.user)


class ExpenseCategoryReportView(ListAPIView):
    """
    API view to retrieve categorized expenses for the current month.
    Groups expenses by category, allowing authenticated users to view categorized reports.
    """
    serializer_class = ExpenseSerializer

    @swagger_auto_schema(
        operation_description="Retrieve categorized expenses for the current month.",
        operation_summary="List Categorized Monthly Expenses",
        tags=["Expenses"],
        responses={
            200: openapi.Response(
                description="A dictionary of expenses categorized by type for the current month",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_ARRAY,
                                                         items=openapi.Items(type=openapi.TYPE_OBJECT))
                )
            ),
            403: openapi.Response("Forbidden - Authentication required")
        }
    )
    def list(self, request, *args, **kwargs):
        """Return expenses grouped by category for the current month."""
        expenses_by_category = request.user.objects.get_expenses_by_category_for_current_month(request.user)
        data = {str(category): ExpenseSerializer(expenses, many=True).data
                for category, expenses in expenses_by_category.items()}
        return Response(data)


class MonthlyStatisticsView(APIView):
    """
    API view to provide monthly statistics for the authenticated user.
    Returns total expenses, remaining balance, and average daily expenditure.
    """

    @swagger_auto_schema(
        operation_description="Retrieve monthly statistics including total expenses, remaining balance, and average daily expenditure.",
        operation_summary="Monthly Financial Statistics",
        tags=["Reports"],
        responses={
            200: openapi.Response(
                description="Monthly financial statistics",
                schema=MonthlyStatisticsSerializer
            ),
            403: openapi.Response("Forbidden - Authentication required")
        }
    )
    def get(self, request, *args, **kwargs):
        """Retrieve financial statistics for the authenticated user's current month."""
        profile = get_object_or_404(Profile, user=request.user)
        stats = Profile.objects.current_month_statistics(user=request.user)
        serializer = MonthlyStatisticsSerializer(stats)
        return Response(serializer.data, status=HTTP_200_OK)
