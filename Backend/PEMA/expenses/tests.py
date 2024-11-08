from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
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
    """

    def setUp(self):
        """
        Set up the test user and category, which are required for creating an expense.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a test category
        self.category = Category.objects.create(name='Food', description='Expenses related to food')
        # Define the URL for the expense creation
        self.url = reverse('api:expenses:expense-create')
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_expense_successful(self):
        """
        Test the successful creation of an expense by an authenticated user.
        """
        # Define the data to create a new expense
        data = {
            'amount': '50.00',
            'category': self.category.id,
            'description': 'Lunch at a restaurant'
        }

        # Send a POST request to create an expense
        response = self.client.post(self.url, data)

        # Assert the response status is HTTP 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the expense object was created in the database
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.first()
        self.assertEqual(expense.amount, 50.00)
        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.category, self.category)
        self.assertEqual(expense.description, 'Lunch at a restaurant')

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
