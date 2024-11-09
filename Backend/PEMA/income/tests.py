from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Income

User = get_user_model()


class IncomeViewTest(APITestCase):
    """
    Test case for creating and updating an Income entry for a user.

    Summary:
    - `test_create_income_successful`: Tests the creation or update of an income entry.
    - `test_create_income_duplicate`: Tests that an existing income entry is updated instead of creating a duplicate.
    - `test_create_income_unauthenticated`: Tests that unauthenticated users cannot access the income entry endpoint.
    """

    def setUp(self):
        """
        Set up the test user required for creating and updating income entries.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Define a single URL for income creation or update
        self.income_url = reverse('api:income:create_or_update_income')
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_income_successful(self):
        """
        Test the successful creation of an income entry by an authenticated user.
        """
        # Define the data to create a new income
        data = {
            'amount': '5000.00',
            'description': 'Monthly salary'
        }

        # Send a PUT request to create or update the income
        response = self.client.put(self.income_url, data)

        # Assert the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the income object was created in the database
        self.assertEqual(Income.objects.count(), 1)
        income = Income.objects.first()
        self.assertEqual(income.amount, 5000.00)
        self.assertEqual(income.user, self.user)
        self.assertEqual(income.description, 'Monthly salary')

    def test_create_income_duplicate(self):
        """
        Test that an existing income entry is updated instead of creating a duplicate.
        """
        # Create an initial income entry for the user
        Income.objects.create(user=self.user, amount=5000.00, description='Monthly salary')

        # Define the data to update the income
        data = {
            'amount': '6000.00',
            'description': 'Bonus'
        }

        # Send a PUT request to update the existing income
        response = self.client.put(self.income_url, data)

        # Assert the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that no additional income object was created in the database
        self.assertEqual(Income.objects.count(), 1)

        # Refresh and verify that the income entry was updated
        income = Income.objects.first()
        self.assertEqual(income.amount, 6000.00)
        self.assertEqual(income.description, 'Bonus')

    def test_create_income_unauthenticated(self):
        """
        Test that unauthenticated users cannot create or update an income entry.
        """
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        # Define the data to create a new income
        data = {
            'amount': '3000.00',
            'description': 'Freelance work'
        }

        # Send a PUT request to attempt to create or update the income
        response = self.client.put(self.income_url, data)

        # Assert the response status is HTTP 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert that no income object was created in the database
        self.assertEqual(Income.objects.count(), 0)

    def test_update_income_non_negative(self):
        """
        Test that a negative income amount is rejected.
        """
        # Define data with a negative amount
        data = {
            'amount': '-1000.00',
            'description': 'Negative income test'
        }

        # Send a PUT request to attempt to create or update the income with a negative amount
        response = self.client.put(self.income_url, data)

        # Assert the response status is HTTP 400 Bad Request due to validation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
