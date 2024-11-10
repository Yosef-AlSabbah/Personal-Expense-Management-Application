from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Income

User = get_user_model()


class IncomeViewTest(APITestCase):
    """
    Test case for updating an existing Income entry for a user.

    Summary:
    - `test_update_income_successful`: Tests the successful update of an income entry.
    - `test_update_income_unauthenticated`: Tests that unauthenticated users cannot access the income entry endpoint.
    - `test_update_income_non_negative`: Tests that a negative income amount is rejected.
    """

    def setUp(self):
        """
        Set up the test user and initial income entry required for updating income entries.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Define the URL for income updates
        self.income_url = reverse('api:income:update_income')
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Create an initial income entry for the user via signal
        Income.objects.create(user=self.user, amount=5000.00, description='Initial income')

    def test_update_income_successful(self):
        """
        Test the successful update of an existing income entry by an authenticated user.
        """
        # Define the data to update the income
        data = {
            'amount': '6000.00',
            'description': 'Updated income'
        }

        # Send a PUT request to update the income
        response = self.client.put(self.income_url, data)

        # Assert the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the income object was updated in the database
        income = Income.objects.get(user=self.user)
        self.assertEqual(income.amount, 6000.00)
        self.assertEqual(income.description, 'Updated income')

    def test_update_income_unauthenticated(self):
        """
        Test that unauthenticated users cannot update an income entry.
        """
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        # Define the data to update the income
        data = {
            'amount': '3000.00',
            'description': 'Freelance work'
        }

        # Send a PUT request to attempt to update the income
        response = self.client.put(self.income_url, data)

        # Assert the response status is HTTP 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_income_non_negative(self):
        """
        Test that a negative income amount is rejected.
        """
        # Define data with a negative amount
        data = {
            'amount': '-1000.00',
            'description': 'Negative income test'
        }

        # Send a PUT request to attempt to update the income with a negative amount
        response = self.client.put(self.income_url, data)

        # Assert the response status is HTTP 400 Bad Request due to validation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
