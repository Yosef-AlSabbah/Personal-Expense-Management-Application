from django.urls import path

from .views import ExpenseReportView, ExpenseCategoryReportView, MonthlyStatisticsView

app_name = 'reports'

urlpatterns = [
    # Endpoint for retrieving the current month's expense report
    path('expenses/monthly/', ExpenseReportView.as_view(), name='expense-monthly-report'),

    # Endpoint for retrieving the current month's expense report grouped by category
    path('expenses/monthly/by-category/', ExpenseCategoryReportView.as_view(),
         name='expense-monthly-by-category-report'),

    # Endpoint for retrieving the monthly statistics of the authenticated user
    # This URL pattern triggers MonthlyStatisticsView, which is used to provide
    # total monthly expenses, remaining balance, and average daily expenditure for the current month.
    path('monthly-statistics/', MonthlyStatisticsView.as_view(), name='monthly-statistics'),

]
