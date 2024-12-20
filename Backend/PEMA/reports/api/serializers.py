from rest_framework import serializers


class MonthlyStatisticsSerializer(serializers.Serializer):
    """
    Serializer for monthly financial statistics, including total expenses, remaining balance, and average daily expenses.
    """

    total_expenses = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total expenses for the current month.",
    )
    remaining_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Remaining balance after subtracting total expenses from income for the current month.",
    )
    average_daily_expense = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Average daily expenditure for the current month.",
    )
