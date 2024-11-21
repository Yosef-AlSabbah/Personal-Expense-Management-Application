import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Profile

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture to initialize the DRF API client."""
    return APIClient()


@pytest.fixture
def test_user():
    """Fixture to create a test user."""
    user = User.objects.create_user(
        email="testuser@example.com",
        password="TestPass123!",
    )
    user.profile.balance = 100
    return user


@pytest.fixture
def auth_client(api_client, test_user):
    """Fixture to authenticate the API client with a test user."""
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


from django.urls import reverse


@pytest.mark.django_db
def test_user_registration(api_client):
    """Test user registration endpoint."""
    url = reverse('api:auth:register')
    response = api_client.post(url, {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "NewPass123!",
        "re_password": "NewPass123!",
        "first_name": "New",
        "last_name": "User",
        "phone_number": "9876543210"
    })
    assert response.status_code == 201
    assert User.objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_user_login(api_client, test_user):
    """Test token obtain pair endpoint."""
    url = reverse('api:auth:jwt-create')
    response = api_client.post(url, {
        "email": test_user.email,
        "password": "TestPass123!"
    })
    assert response.status_code == 200
    assert "access" in response.data["data"]  # Adjust to access the token correctly
    assert "refresh" in response.data["data"]


@pytest.mark.django_db
def test_user_profile_retrieve(auth_client):
    """Test the `me` endpoint to retrieve the profile."""
    url = reverse('api:auth:current_user')
    response = auth_client.get(url)
    print(response.data)  # Debugging to inspect the structure of response data
    assert response.status_code == 200
    assert response.data['data']['email'] == "testuser@example.com"  # Check email too


@pytest.mark.django_db
def test_user_profile_update(auth_client):
    """Test updating the user profile via the `me` endpoint."""
    url = reverse('api:auth:current_user')  # Dynamically resolve the URL for the `me` endpoint
    response = auth_client.patch(url, {
        "first_name": "Updated",
        "last_name": "User",
        "phone_number": "0987654321"
    })
    print(response.data)  # Debugging to inspect the response structure
    assert response.status_code == 200
    assert response.data['data']['first_name'] == "Updated"
    assert response.data['data']['last_name'] == "User"
    assert response.data['data']['phone_number'] == "0987654321"


@pytest.mark.django_db
def test_user_profile_delete(auth_client):
    """Test deleting the authenticated user's profile."""
    url = reverse('api:auth:current_user')  # Use reverse() for dynamic URL resolution
    response = auth_client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_password_reset_request(api_client, test_user):
    """Test initiating a password reset."""
    url = reverse('api:auth:reset_password')  # Ensure this matches the `name` in your URL config
    response = api_client.post(url, {
        "email": test_user.email
    })
    print(response.data)  # Debugging to inspect the response structure
    assert response.status_code == 204  # Update to match the actual status code


@pytest.mark.django_db
def test_token_refresh(api_client, test_user):
    """Test refreshing an access token."""
    refresh = RefreshToken.for_user(test_user)
    url = reverse('api:auth:jwt-refresh')
    response = api_client.post(url, {
        "refresh": str(refresh)
    })
    print(response.data)  # Debugging to inspect the response structure
    assert response.status_code == 200
    assert "access" in response.data['data']  # Ensure the new access token is returned


@pytest.mark.django_db
def test_token_blacklist(auth_client):
    """Test blacklisting a refresh token (logout)."""
    response = auth_client.post(reverse('api:auth:jwt-destroy'), {
        "refresh": "dummy-refresh-token"
    })
    assert response.status_code == 400  # Expect failure with dummy token


@pytest.mark.django_db
def test_profile_manager_current_month_statistics(test_user):
    """Test custom ProfileManager statistics calculation."""
    stats = Profile.objects.current_month_statistics(test_user)  # Access manager via model class
    assert "total_expenses" in stats
    assert "remaining_balance" in stats
    assert "average_daily_expense" in stats
