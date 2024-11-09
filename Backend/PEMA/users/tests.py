from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Profile

User = get_user_model()

class UserProfileUpdateTestCase(TestCase):
    def setUp(self):
        # Set up a test user and profile
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User',
            email='testuser@example.com'
        )
        self.profile = Profile.objects.create(user=self.user, balance=100.0)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.update_url = reverse('api:users:profile-update')

    def test_update_profile_successfully(self):
        # Define the payload for updating the user profile
        payload = {
            "user": {
                "first_name": "Updated",
                "last_name": "User",
                "email": "updateduser@example.com"
            },
            "profile": {
                "profile_pic": None  # Assuming no file is uploaded for simplicity
            }
        }

        response = self.client.put(self.update_url, payload, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reload the user and profile from the database
        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        # Check that the fields have been updated
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.email, "updateduser@example.com")

    def test_update_profile_unauthenticated(self):
        # Log out the user
        self.client.force_authenticate(user=None)

        payload = {
            "user": {
                "first_name": "New",
                "last_name": "Name",
                "email": "newname@example.com"
            },
            "profile": {
                "profile_pic": None
            }
        }

        response = self.client.put(self.update_url, payload, format='json')

        # Ensure the response status is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_invalid_email(self):
        payload = {
            "user": {
                "first_name": "Updated",
                "last_name": "User",
                "email": "not-an-email"
            },
            "profile": {
                "profile_pic": None
            }
        }

        response = self.client.put(self.update_url, payload, format='json')

        # Ensure the response status is bad request due to invalid email format
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['user'])

    def test_partial_update_profile(self):
        payload = {
            "user": {
                "first_name": "PartiallyUpdated"
            }
        }

        response = self.client.patch(self.update_url, payload, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reload the user from the database and check the field has been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "PartiallyUpdated")
