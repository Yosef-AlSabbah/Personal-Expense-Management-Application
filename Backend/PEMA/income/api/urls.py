from django.urls import path

from .views import UpdateIncomeView

app_name = 'income'

urlpatterns = [
    path('update/', UpdateIncomeView.as_view(), name='update_income'),
]
