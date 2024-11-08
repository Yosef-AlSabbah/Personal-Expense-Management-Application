from django.urls import path

from .views import CreateIncomeView, UpdateIncomeView

# Namespacing the URL patterns for the 'income' app
app_name = 'income'

urlpatterns = [
    # This view is used to create an income record for the authenticated user.
    path('create/', CreateIncomeView.as_view(), name='create_income'),

    # This view allows the authenticated user to update their existing income record.
    path('update/', UpdateIncomeView.as_view(), name='update_income'),
]
