# reports/tests.py

from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from expenses.models import Expense, Category

User = get_user_model()


# Fixtures

@pytest.fixture
def test_user(db):
    """Fixture to create a test user with profile and income."""
    user = User.objects.create_user(
        email='testuser@example.com',
        password='testpassword'
    )
    # Assuming User has a related Profile model
    user.profile.balance = Decimal('5000.00')
    user.profile.save()
    # Assuming User has a related Income model
    user.income.amount = Decimal('5000.00')
    user.income.save()
    return user


@pytest.fixture
def food_category(db):
    """Fixture to create a 'Food' category."""
    return Category.objects.create(name='Food')


@pytest.fixture
def transport_category(db):
    """Fixture to create a 'Transport' category."""
    return Category.objects.create(name='Transport')


@pytest.fixture
def expenses(db, test_user, food_category, transport_category):
    """Fixture to create expenses for the current month."""
    today = date.today()
    expense1 = Expense.objects.create(
        user=test_user,
        amount=Decimal('100.00'),
        category=food_category,
        date=today
    )
    expense2 = Expense.objects.create(
        user=test_user,
        amount=Decimal('50.00'),
        category=transport_category,
        date=today
    )
    return [expense1, expense2]


@pytest.fixture
def expense_monthly_url():
    """Fixture for the expense monthly report URL."""
    return reverse('api:reports:expense-monthly-report')


@pytest.fixture
def expense_category_url():
    """Fixture for the expense category-based report URL."""
    return reverse('api:reports:expense-monthly-by-category-report')


@pytest.fixture
def monthly_statistics_url():
    """Fixture for the monthly statistics URL."""
    return reverse('api:reports:monthly-statistics')


@pytest.fixture
def auth_client(db, test_user):
    """Fixture to provide an authenticated API client."""
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


# Test Functions

@pytest.mark.django_db
def test_expense_monthly_report(auth_client, expense_monthly_url, expenses):
    """
    Test retrieving the current month's expense report for the authenticated user.
    """
    response = auth_client.get(expense_monthly_url)

    # Ensure status is HTTP 200 OK
    assert response.status_code == 200

    # Assert the response contains data as a flat list
    assert 'data' in response.data
    assert len(response.data['data']) == 2

    # Validate individual entries in the response data
    expected_amounts = {Decimal('100.00'), Decimal('50.00')}
    response_amounts = {Decimal(item['amount']) for item in response.data['data']}
    assert response_amounts == expected_amounts


@pytest.mark.django_db
def test_expense_category_report(auth_client, expense_category_url, expenses):
    """
    Test retrieving the current month's expense report grouped by category for the authenticated user.
    """
    response = auth_client.get(expense_category_url)

    # Assert the response status is HTTP 200 OK
    assert response.status_code == 200

    # Assert that the response contains the correct categories and expenses
    assert 'data' in response.data
    assert 'Food' in response.data['data']
    assert 'Transport' in response.data['data']
    assert len(response.data['data']['Food']) == 1
    assert len(response.data['data']['Transport']) == 1

    # Validate the amounts
    assert Decimal(response.data['data']['Food'][0]['amount']) == Decimal('100.00')
    assert Decimal(response.data['data']['Transport'][0]['amount']) == Decimal('50.00')


@pytest.mark.django_db
def test_monthly_statistics_view(auth_client, monthly_statistics_url, expenses):
    """
    Test retrieving the monthly statistics for the authenticated user.
    """
    response = auth_client.get(monthly_statistics_url)

    # Ensure status is HTTP 200 OK
    assert response.status_code == 200

    # Validate that the response contains correct data
    assert 'data' in response.data

    # Extract and validate statistics from the response
    data = response.data['data']
    assert 'total_expenses' in data
    assert 'remaining_balance' in data
    assert 'average_daily_expense' in data

    # Assert the values match expected calculations
    assert Decimal(data['total_expenses']) == Decimal('150.00')
    assert Decimal(data['remaining_balance']) == Decimal('4850.00')
    assert float(data['average_daily_expense']) >= 0.0


@pytest.mark.django_db
def test_expense_report_unauthenticated(client, expense_monthly_url, expense_category_url, monthly_statistics_url):
    """
    Test that unauthenticated users cannot access the expense report views.
    """
    # Attempt to access each report view without authentication
    response_monthly = client.get(expense_monthly_url)
    response_category = client.get(expense_category_url)
    response_statistics = client.get(monthly_statistics_url)

    # Assert all responses return HTTP 401 Unauthorized
    assert response_monthly.status_code == 401
    assert response_category.status_code == 401
    assert response_statistics.status_code == 401
