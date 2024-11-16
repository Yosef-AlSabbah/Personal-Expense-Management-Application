from django.urls import path

from .views import ExpenseCreateView

app_name = 'expenses'

urlpatterns = [
    # Define URL patterns for the expenses app. Currently, it only contains a URL pattern for creating a new expense.
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
]
