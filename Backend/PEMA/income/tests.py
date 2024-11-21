# income/tests.py

from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Profile
from .models import Income

User = get_user_model()


# Fixtures

@pytest.fixture
def user(db):
    """Fixture to create a test user."""
    return User.objects.create_user(email='testuser@example.com', password='testpass123')


@pytest.fixture
def income(db, user):
    """Fixture to create the user's income."""
    income, created = Income.objects.get_or_create(
        user=user,
        defaults={'amount': Decimal('500.00'), 'description': 'Initial income'}
    )
    # Ensure the amount is set correctly if the instance already exists
    if not created and income.amount != Decimal('500.00'):
        income.amount = Decimal('500.00')
        income.description = 'Initial income'
        income.save()
    return income


@pytest.fixture
def profile(db, user, income):
    """Fixture to create the user's profile and set the correct balance."""
    profile, created = Profile.objects.get_or_create(user=user)
    profile.update_balance()  # This sets the balance based on income and expenses
    return profile


@pytest.fixture
def auth_client(db, user):
    """Fixture to provide an authenticated API client using JWT."""
    client = APIClient()
    # Generate JWT token for the user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    # Set the Authorization header
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.fixture
def unauthenticated_client(db):
    """Fixture to provide an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def update_income_url():
    """Fixture for the update income URL."""
    return reverse('api:income:update_income')  # Ensure this URL name is correct


# Test Functions

@pytest.mark.django_db
def test_put_update_income_success(auth_client, update_income_url, income, profile):
    """Test successful PUT request to update income."""
    data = {
        "amount": "600.00",
        "description": "Updated income via PUT"
    }

    response = auth_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['amount'] == "600.00"
    assert response.data['data']['description'] == "Updated income via PUT"

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Verify income updates
    assert income.amount == Decimal('600.00')
    assert income.description == "Updated income via PUT"

    # Profile balance should now equal the new income amount minus expenses
    # Assuming no expenses, balance should be 600.00
    assert profile.balance == Decimal('600.00')


@pytest.mark.django_db
def test_patch_update_income_success(auth_client, update_income_url, income, profile):
    """Test successful PATCH request to update income."""
    data = {
        "description": "Partially updated income via PATCH"
    }

    response = auth_client.patch(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['description'] == "Partially updated income via PATCH"

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Verify income description update
    assert income.description == "Partially updated income via PATCH"

    # Ensure profile balance remains unchanged (since amount wasn't changed)
    assert profile.balance == Decimal('500.00')


@pytest.mark.django_db
def test_put_update_income_invalid_amount(auth_client, update_income_url, income, profile):
    """Test PUT request with invalid amount (<= 0)."""
    data = {
        "amount": "-100.00",
        "description": "Invalid income amount"
    }

    response = auth_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["status"] == "error"
    assert response.data["data"] is None  # Ensure data is None
    assert "errors" in response.data
    assert "amount" in response.data["errors"]
    assert response.data["errors"]["amount"][0] == "Income amount must be greater than zero."

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Ensure income amount remains unchanged
    assert income.amount == Decimal("500.00")
    # Ensure profile balance remains unchanged
    assert profile.balance == Decimal("500.00")


@pytest.mark.django_db
def test_patch_update_income_invalid_amount(auth_client, update_income_url, income, profile):
    """Test PATCH request with invalid amount (<= 0)."""
    data = {
        "amount": "0.00"
    }

    response = auth_client.patch(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["status"] == "error"
    assert response.data["data"] is None  # Ensure data is None
    assert "errors" in response.data
    assert "amount" in response.data["errors"]
    assert response.data["errors"]["amount"][0] == "Income amount must be greater than zero."

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Ensure income amount remains unchanged
    assert income.amount == Decimal("500.00")
    # Ensure profile balance remains unchanged
    assert profile.balance == Decimal("500.00")


@pytest.mark.django_db
def test_update_income_no_income_entry(auth_client, update_income_url, user, profile):
    """Test updating income when the user has no income entry."""
    # Delete the existing income entry
    Income.objects.filter(user=user).delete()

    data = {
        "amount": "700.00",
        "description": "Attempt to update non-existing income"
    }

    response = auth_client.put(update_income_url, data, format='json')

    print("Response Data:", response.data)  # For debugging

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["status"] == "error"
    assert response.data["data"] is None  # Ensure data is None
    assert "errors" in response.data
    assert "error" in response.data["errors"]
    assert response.data["errors"]["error"] == "Income entry does not exist for this user."

    # Ensure profile balance remains unchanged
    profile.refresh_from_db()
    assert profile.balance == Decimal("500.00")


@pytest.mark.django_db
def test_update_income_unauthenticated(unauthenticated_client, update_income_url, profile):
    """Test updating income without authentication."""
    data = {
        "amount": "600.00",
        "description": "Unauthenticated update attempt"
    }

    response = unauthenticated_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["status"] == "error"
    assert response.data["data"] is None  # Ensure data is None

    assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_update_income_profile_not_exists(auth_client, update_income_url, user, income):
    """Test updating income when the user's profile does not exist."""
    # Delete the profile
    Profile.objects.filter(user=user).delete()

    data = {
        "amount": "600.00",
        "description": "Update without profile"
    }

    response = auth_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["status"] == "error"
    assert response.data["data"] is None  # Ensure data is None
    assert "errors" in response.data  # Check errors exist
    assert "error" in response.data["errors"]
    assert response.data["errors"]["error"] == "User profile does not exist."


@pytest.mark.django_db
def test_update_income_no_amount_change_profile_not_updated(auth_client, update_income_url, income, profile):
    """Test that profile balance is not updated when the income amount does not change."""
    data = {
        "description": "No amount change"
    }

    response = auth_client.patch(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_200_OK

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Ensure income description is updated
    assert income.description == "No amount change"

    # Ensure profile balance remains unchanged
    assert profile.balance == Decimal('500.00')


@pytest.mark.django_db
def test_update_income_amount_change_profile_updated(auth_client, update_income_url, income, profile):
    """Test that profile balance is updated when the income amount changes."""
    data = {
        "amount": "700.00",
        "description": "Amount changed to trigger profile update"
    }

    response = auth_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_200_OK

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Verify income updates
    assert income.amount == Decimal('700.00')
    assert income.description == "Amount changed to trigger profile update"

    # Profile balance should now equal the new income amount minus expenses
    # Assuming no expenses, balance should be 700.00
    assert profile.balance == Decimal('700.00')  # Corrected expectation


@pytest.mark.django_db
def test_update_income_invalid_description(auth_client, update_income_url, income, profile):
    """Test updating income with invalid description (e.g., excessively long)."""
    data = {
        "amount": "600.00",
        "description": "a" * 1001  # Invalid description exceeding max_length
    }

    response = auth_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["status"] == "error"
    assert response.data["data"] is None  # Ensure data is None
    assert "errors" in response.data
    assert "description" in response.data["errors"]
    assert response.data["errors"]["description"][0] == "Ensure this field has no more than 1000 characters."


@pytest.mark.django_db
def test_update_income_extra_fields_ignored(auth_client, update_income_url, income, profile):
    """Test that extra fields in the request are ignored."""
    data = {
        "amount": "600.00",
        "description": "Valid update",
        "extra_field": "This should be ignored"
    }

    response = auth_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'extra_field' not in response.data['data']  # Ensure extra fields are ignored

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Verify income updates
    assert income.amount == Decimal('600.00')
    assert income.description == "Valid update"

    # Ensure profile balance is updated accordingly
    # Original income: 500.00, new income: 600.00 => difference: +100.00
    assert profile.balance == Decimal('600.00')


@pytest.mark.django_db
def test_update_income_read_only_fields_immutable(auth_client, update_income_url, income, profile):
    """Test that read-only fields cannot be updated."""
    data = {
        "amount": "600.00",
        "date": "2023-01-01",
        "last_updated": "2023-01-01T00:00:00Z",
        "summary": "Attempting to change read-only fields"
    }

    response = auth_client.put(update_income_url, data, format='json')

    assert response.status_code == status.HTTP_200_OK

    # Refresh instances from the database
    income.refresh_from_db()
    profile.refresh_from_db()

    # Ensure read-only fields have not changed
    assert str(income.date) != "2023-01-01"
    assert str(income.last_updated.date()) != "2023-01-01"
    assert income.summary != "Attempting to change read-only fields"

    # Also, verify the response data does not include the updated read-only fields
    assert response.data.get('date') != "2023-01-01"
    assert response.data.get('last_updated') != "2023-01-01T00:00:00Z"
    assert response.data.get('summary') != "Attempting to change read-only fields"
