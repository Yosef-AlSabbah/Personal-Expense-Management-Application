from django.urls import path

# Import views for expense management
from .views import ExpenseCreateView

# Application namespace to avoid conflicts
app_name = 'expenses'

urlpatterns = [
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ EXPENSES URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Endpoint to create a new expense
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
]
