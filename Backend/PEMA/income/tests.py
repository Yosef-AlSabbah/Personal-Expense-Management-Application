from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Income

User = get_user_model()


class IncomeViewTest(APITestCase):
    """
    Test case for creating and updating an Income entry for a user.

    Summary:
    - `test_create_income_successful`: Tests the successful creation of an income entry.
    - `test_create_income_duplicate`: Tests that duplicate income entries cannot be created for a user.
    - `test_create_income_unauthenticated`: Tests that unauthenticated users cannot create income entries.
    - `test_update_income_successful`: Tests the successful update of an existing income entry.
    - `test_update_income_unauthenticated`: Tests that unauthenticated users cannot update an income entry.
    - `test_update_income_does_not_exist`: Tests that updating an income fails if no income entry exists for the user.
    """

    def setUp(self):
        """
        Set up the test user which is required for creating and updating income entries.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Define URLs for income creation and update
        self.create_url = reverse('api:income:create_income')
        self.update_url = reverse('api:income:update_income')
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_income_successful(self):
        """
        Test the successful creation of an income by an authenticated user.
        """
        # Define the data to create a new income
        data = {
            'amount': '5000.00',
            'description': 'Monthly salary'
        }

        # Send a POST request to create an income
        response = self.client.post(self.create_url, data)

        # Assert the response status is HTTP 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the income object was created in the database
        self.assertEqual(Income.objects.count(), 1)
        income = Income.objects.first()
        self.assertEqual(income.amount, 5000.00)
        self.assertEqual(income.user, self.user)
        self.assertEqual(income.description, 'Monthly salary')

    def test_create_income_duplicate(self):
        """
        Test that an income cannot be created if one already exists for the user.
        """
        # Create an initial income entry for the user
        Income.objects.create(user=self.user, amount=5000.00, description='Monthly salary')

        # Define the data to create a duplicate income
        data = {
            'amount': '6000.00',
            'description': 'Bonus'
        }

        # Send a POST request to create a duplicate income
        response = self.client.post(self.create_url, data)

        # Assert the response status is HTTP 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that no additional income object was created in the database
        self.assertEqual(Income.objects.count(), 1)

    def test_create_income_unauthenticated(self):
        """
        Test that unauthenticated users cannot create an income.
        """
        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        # Define the data to create a new income
        data = {
            'amount': '3000.00',
            'description': 'Freelance work'
        }

        # Send a POST request to create an income
        response = self.client.post(self.create_url, data)

        # Assert the response status is HTTP 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert that no income object was created in the database
        self.assertEqual(Income.objects.count(), 0)

    def test_update_income_successful(self):
        """
        Test the successful update of an existing income by an authenticated user.
        """
        # Create an initial income entry for the user
        income = Income.objects.create(user=self.user, amount=5000.00, description='Monthly salary')

        # Define the data to update the income
        data = {
            'amount': '6000.00',
            'description': 'Updated salary'
        }

        # Send a PUT request to update the income
        response = self.client.put(self.update_url, data)

        # Assert the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the income instance from the database
        income.refresh_from_db()
        self.assertEqual(income.amount, 6000.00)
        self.assertEqual(income.description, 'Updated salary')

    def test_update_income_unauthenticated(self):
        """
        Test that unauthenticated users cannot update an income.
        """
        # Create an initial income entry for the user
        Income.objects.create(user=self.user, amount=5000.00, description='Monthly salary')

        # Remove the credentials to simulate an unauthenticated request
        self.client.credentials()

        # Define the data to update the income
        data = {
            'amount': '7000.00',
            'description': 'Freelance payment'
        }

        # Send a PUT request to update the income
        response = self.client.put(self.update_url, data)

        # Assert the response status is HTTP 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_income_does_not_exist(self):
        """
        Test that updating an income fails if no income exists for the user.
        """
        # Define the data to update the income
        data = {
            'amount': '8000.00',
            'description': 'Freelance payment'
        }

        # Send a PUT request to update the income
        response = self.client.put(self.update_url, data)

        # Assert the response status is HTTP 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
