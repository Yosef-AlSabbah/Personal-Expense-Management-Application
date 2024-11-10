from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Profile
from .models import Expense, Category

User = get_user_model()


class ExpenseCreateViewTest(APITestCase):
    """
    Test case for creating and updating an Income entry for a user.

    Summary:
    - `test_create_expense_successful`: Tests successful creation of an expense with valid data.
    - `test_create_expense_unauthenticated`: Tests that unauthenticated users cannot create an expense.
    - `test_create_expense_invalid_amount`: Tests that an expense with a non-positive amount cannot be created.
    - `test_create_expense_missing_category`: Tests that an expense cannot be created without specifying a category.
    - `test_create_expense_missing_amount`: Tests that an expense cannot be created without specifying an amount.
    - `test_create_expense_insufficient_balance`: Tests that an expense cannot be created if the user's balance is insufficient.
    """

    def setUp(self):
        """
        Set up the test user and category, which are required for creating an expense.
        """
        # Create a test user and profile with initial balance
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, balance=100.00)  # Set initial balance
        self.category = Category.objects.create(name='Food', description='Expenses related to food')
        self.url = reverse('api:expenses:expense-create')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_expense_successful(self):
        """Test the successful creation of an expense by an authenticated user."""
        data = {
            'amount': '50.00',
            'category_id': self.category.id,
            'description': 'Lunch at a restaurant'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.first()
        self.assertEqual(expense.amount, 50.00)
        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.category, self.category)
        self.assertEqual(expense.description, 'Lunch at a restaurant')

    def test_create_expense_insufficient_balance(self):
        """
        Test that an expense cannot be created if the user's balance is insufficient.
        """
        data = {
            'amount': '150.00',  # Amount exceeds user's balance
            'category_id': self.category.id,
            'description': 'Expensive dinner'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient balance", str(response.data))  # Check for the error message
        self.assertEqual(Expense.objects.count(), 0)

    def test_create_expense_sufficient_balance(self):
        """
        Test that an expense can be created if the user's balance is sufficient.
        """
        data = {
            'amount': '50.00',  # Amount within user's balance
            'category_id': self.category.id,
            'description': 'Affordable dinner'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)

        # Verify that balance is updated correctly
        self.profile.refresh_from_db()  # Reload profile to get updated balance
        self.assertEqual(self.profile.balance, 50.00)  # Balance after deduction

    def test_create_expense_unauthenticated(self):
        """
        Test that unauthenticated users cannot create an expense.
        """
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        # Define the data to create a new expense
        data = {
            'amount': '30.00',
            'category': self.category.id,
            'description': 'Dinner'
        }

        # Send a POST request to create an expense
        response = self.client.post(self.url, data)

        # Assert the response status is HTTP 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert that no expense object was created in the database
        self.assertEqual(Expense.objects.count(), 0)

    def test_create_expense_invalid_amount(self):
        """
        Test that an expense with a non-positive amount cannot be created.
        """
        # Define the data with an invalid amount (e.g., negative value)
        data = {
            'amount': '-10.00',
            'category': self.category.id,
            'description': 'Groceries'
        }

        # Send a POST request to create an expense
        response = self.client.post(self.url, data)

        # Assert the response status is HTTP 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that no expense object was created in the database
        self.assertEqual(Expense.objects.count(), 0)

    def test_create_expense_missing_category(self):
        """
        Test that an expense cannot be created without specifying a category.
        """
        # Define the data without the category field
        data = {
            'amount': '40.00',
            'description': 'Taxi ride'
        }

        # Send a POST request to create an expense
        response = self.client.post(self.url, data)

        # Assert the response status is HTTP 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that no expense object was created in the database
        self.assertEqual(Expense.objects.count(), 0)

    def test_create_expense_missing_amount(self):
        """
        Test that an expense cannot be created without specifying an amount.
        """
        # Define the data without the amount field
        data = {
            'category': self.category.id,
            'description': 'Groceries'
        }

        # Send a POST request to create an expense
        response = self.client.post(self.url, data)

        # Assert the response status is HTTP 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that no expense object was created in the database
        self.assertEqual(Expense.objects.count(), 0)
