from django.urls import path

from .views import ExpenseCreateView

app_name = 'expenses'

urlpatterns = [
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
]
