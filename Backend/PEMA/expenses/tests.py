from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Category, Expense

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture for the DRF API client."""
    return APIClient()


@pytest.fixture
def test_user():
    """Fixture to create a test user."""
    user = User.objects.create_user(
        email="testuser@example.com",
        password="TestPass123!",
    )
    user.profile.balance = 1000  # Set an initial balance
    user.profile.save()
    return user


@pytest.fixture
def auth_client(api_client, test_user):
    """Fixture to authenticate the API client with a test user."""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def test_category():
    """Fixture to create a test category."""
    return Category.objects.create(name="Food", description="Food-related expenses")


@pytest.fixture
def test_expense(test_user, test_category):
    """Fixture to create a test expense."""
    return Expense.objects.create(
        user=test_user,
        amount=100,
        category=test_category,
        description="Grocery shopping"
    )


@pytest.mark.django_db
def test_category_creation():
    """Test category creation and string representation."""
    category = Category.objects.create(name="Transport", description="Travel-related expenses")
    assert str(category) == "Transport"
    assert category.title == "Transport"


@pytest.mark.django_db
def test_expense_creation(test_user, test_category):
    """Test creating an expense."""
    expense = Expense.objects.create(
        user=test_user,
        amount=50.00,
        category=test_category,
        description="Lunch at a restaurant"
    )
    assert str(expense) == f"{test_user} spent 50.00 on {expense.date}"
    assert expense.summary == f"Expense of 50.00 in {test_category}"


@pytest.mark.django_db
def test_get_expenses_for_current_month(test_user, test_expense):
    """Test manager method to get expenses for the current month."""
    current_month_expenses = Expense.objects.get_expenses_for_current_month(test_user)
    assert len(current_month_expenses) == 1
    assert current_month_expenses[0] == test_expense


@pytest.mark.django_db
def test_get_expenses_by_category_for_current_month(test_user, test_expense):
    """Test manager method to group expenses by category for the current month."""
    expenses_by_category = Expense.objects.get_expenses_by_category_for_current_month(test_user)
    assert len(expenses_by_category) == 1
    assert test_expense.category in expenses_by_category
    assert test_expense in expenses_by_category[test_expense.category]


@pytest.mark.django_db
def test_api_create_expense(auth_client, test_category):
    """Test API endpoint to create an expense."""
    url = reverse('api:expenses:expense-create')
    payload = {
        "amount": 150.00,
        "category_id": test_category.id,
        "description": "Dinner with friends"
    }
    response = auth_client.post(url, payload, format="json")
    assert response.status_code == 201
    assert response.data["message"] == "Expense created successfully."
    assert Expense.objects.filter(description="Dinner with friends").exists()


@pytest.mark.django_db
def test_expense_creation_insufficient_balance(auth_client, test_category, test_user):
    """Test API endpoint to create an expense with insufficient balance."""
    # Set the user's balance lower than the expense amount
    test_user.profile.balance = Decimal(20)
    test_user.profile.save()

    url = reverse('api:expenses:expense-create')
    payload = {
        "amount": 100.00,  # Amount exceeds the balance
        "category_id": test_category.id,
        "description": "Expensive dinner"
    }

    response = auth_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "Insufficient balance" in response.data["message"]

    # Ensure that the expense was not created
    assert not Expense.objects.filter(description="Expensive dinner").exists()


@pytest.mark.django_db
def test_api_create_expense_invalid_category(auth_client):
    """Test API endpoint to create an expense with an invalid category."""
    url = reverse('api:expenses:expense-create')
    payload = {
        "amount": 150.00,
        "category_id": 9999,  # Non-existent category ID
        "description": "Invalid category"
    }
    response = auth_client.post(url, payload, format="json")
    assert response.status_code == 400
    assert "Invalid pk" in str(response.data)
