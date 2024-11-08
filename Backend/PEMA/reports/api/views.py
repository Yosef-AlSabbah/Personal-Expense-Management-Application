from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of expenses for the current month, filtered by the authenticated user.
        """
        return Expense.objects.get_expenses_for_current_month(user=self.request.user).filter(user=self.request.user)


class ExpenseCategoryReportView(ListAPIView):
    """
    API view to retrieve a categorized list of expenses for the current month.
    Groups expenses by category, allowing authenticated users to view categorized reports.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to return expenses grouped by category for the current month.
        """
        expenses_by_category = Expense.objects.get_expenses_by_category_for_current_month(user=self.request.user)

        # Convert the grouped data to a serialized format, using category names as keys
        data = {str(category): ExpenseSerializer(expenses, many=True).data
                for category, expenses in expenses_by_category.items()}

        return Response(data)


class MonthlyStatisticsView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        # Get the monthly statistics using the ProfileManager
        stats = Profile.objects.current_month_statistics(user)

        # Serialize the stats to return as response
        serializer = MonthlyStatisticsSerializer(stats)
        return Response(serializer.data, status=HTTP_200_OK)
