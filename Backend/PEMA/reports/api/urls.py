from django.urls import path

from .views import ExpenseReportView, ExpenseCategoryReportView

app_name = 'reports'

urlpatterns = [
    # Endpoint for retrieving the current month's expense report
    path('expenses/monthly/', ExpenseReportView.as_view(), name='expense-monthly-report'),

    # Endpoint for retrieving the current month's expense report grouped by category
    path('expenses/monthly/by-category/', ExpenseCategoryReportView.as_view(),
         name='expense-monthly-by-category-report'),
]
