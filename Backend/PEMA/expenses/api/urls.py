from django.urls import path
from .views import ExpenseCreateView

# Namespacing the URL patterns for the 'expenses' app
app_name = 'expenses'

urlpatterns = [
    # Endpoint for creating a new expense entry
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
]
