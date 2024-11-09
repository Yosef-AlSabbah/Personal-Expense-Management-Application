from django.urls import path

from .views import CreateOrUpdateIncomeView

app_name = 'income'

urlpatterns = [
    path('', CreateOrUpdateIncomeView.as_view(), name='create_or_update_income'),
]
