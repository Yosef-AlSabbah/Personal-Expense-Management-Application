from rest_framework import serializers


# MonthlyStatisticsSerializer is a serializer that handles the conversion of
# monthly statistics data (i.e., total expenses, remaining balance, and average daily expense)
# into a suitable JSON format that can be returned by a REST API view.
class MonthlyStatisticsSerializer(serializers.Serializer):
    # Total expenses for the current month. This field expects a decimal value.
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)

    # Remaining balance for the current month after deducting the total expenses
    # from the user's income.
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    # Average daily expenditure for the current month, calculated by dividing
    # the total monthly expenses by the number of days in the month so far.
    average_daily_expense = serializers.DecimalField(max_digits=10, decimal_places=2)
