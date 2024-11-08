from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from expenses.api.serializers import ExpenseSerializer
from expenses.models import Expense


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
        return Expense.objects.get_expenses_for_current_month(user=self.request.user)


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

        # Convert the grouped data to a serialized format
        data = {category: ExpenseSerializer(expenses, many=True).data
                for category, expenses in expenses_by_category.items()}

        return Response(data)
