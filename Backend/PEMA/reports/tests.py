from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from expenses.models import Expense, Category
from income.models import Income
from users.models import Profile

User = get_user_model()


class ExpenseReportTest(APITestCase):
    """
    Test case for the expense report views including monthly reports, category-based reports, and monthly statistics.

    Summary:
    - `test_expense_monthly_report`: Tests retrieving the current month's expenses for the authenticated user.
    - `test_expense_category_report`: Tests retrieving expenses grouped by category for the current month.
    - `test_monthly_statistics_view`: Tests retrieving the monthly statistics including total expenses, remaining balance, and average daily expense.
    - `test_expense_report_unauthenticated`: Tests that unauthenticated users cannot access the expense report views.
    """

    def setUp(self):
        """
        Set up the test user, profile, categories, and expenses required for testing.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a profile for the user
        self.profile = Profile.objects.create(user=self.user, balance=5000.00)
        # Create an income entry for the user
        self.income = Income.objects.create(user=self.user, amount=5000.00)
        # Create categories
        self.food_category = Category.objects.create(name='Food')
        self.transport_category = Category.objects.create(name='Transport')
        # Create expenses for the current month
        today = date.today()
        Expense.objects.create(user=self.user, amount=100.00, category=self.food_category, date=today)
        Expense.objects.create(user=self.user, amount=50.00, category=self.transport_category, date=today)
        # Define URLs for expense report views
        self.expense_monthly_url = reverse('api:reports:expense-monthly-report')
        self.expense_category_url = reverse('api:reports:expense-monthly-by-category-report')
        self.monthly_statistics_url = reverse('api:reports:monthly-statistics')
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_expense_monthly_report(self):
        """
        Test retrieving the current month's expense report for the authenticated user.
        """
        # Set the JWT token in credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.expense_monthly_url)

        # Assert the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the correct number of expenses in 'results'
        self.assertEqual(len(response.data['results']), 2)

        # Validate the actual values inside the results to ensure correctness
        self.assertEqual(response.data['results'][0]['amount'], '100.00')
        self.assertEqual(response.data['results'][1]['amount'], '50.00')

    def test_expense_category_report(self):
        """
        Test retrieving the current month's expense report grouped by category for the authenticated user.
        """
        # Send a GET request to retrieve the category-based expense report
        response = self.client.get(self.expense_category_url)

        # Assert the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the correct categories and expenses
        self.assertIn('Food', response.data)
        self.assertIn('Transport', response.data)
        self.assertEqual(len(response.data['Food']), 1)
        self.assertEqual(len(response.data['Transport']), 1)
        self.assertEqual(response.data['Food'][0]['amount'], '100.00')
        self.assertEqual(response.data['Transport'][0]['amount'], '50.00')

    def test_monthly_statistics_view(self):
        """
        Test retrieving the monthly statistics for the authenticated user.
        """
        # Send a GET request to retrieve the monthly statistics
        response = self.client.get(self.monthly_statistics_url)

        # Assert the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the correct statistics
        self.assertIn('total_expenses', response.data)
        self.assertIn('remaining_balance', response.data)
        self.assertIn('average_daily_expense', response.data)
        self.assertEqual(str(response.data['total_expenses']), '150.00')
        self.assertEqual(str(response.data['remaining_balance']), '4850.00')
        self.assertGreaterEqual(float(response.data['average_daily_expense']), 0.0)

    def test_expense_report_unauthenticated(self):
        """
        Test that unauthenticated users cannot access the expense report views.
        """
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        # Attempt to access each report view
        response_monthly = self.client.get(self.expense_monthly_url)
        response_category = self.client.get(self.expense_category_url)
        response_statistics = self.client.get(self.monthly_statistics_url)

        # Assert all responses return HTTP 401 Unauthorized
        self.assertEqual(response_monthly.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_category.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_statistics.status_code, status.HTTP_401_UNAUTHORIZED)
