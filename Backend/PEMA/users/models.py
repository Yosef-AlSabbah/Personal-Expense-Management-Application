from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from users.utils import get_unique_profile_pic_path

User = get_user_model()


class ProfileManager(models.Manager):
    def current_month_statistics(self, user):
        """
        Provides the monthly statistics for the given user:
        - Total monthly expenses
        - Remaining balance
        - Average daily expenditure
        """
        today = timezone.now().date()
        start_of_month = today.replace(day=1)

        # Get user's expenses for the current month
        expenses = user.expenses.filter(date__gte=start_of_month)
        total_expenses = sum(expense.amount for expense in expenses)

        # Calculate remaining balance
        income = getattr(user, 'income', None)
        remaining_balance = (income.amount if income else 0) - total_expenses

        # Calculate average daily expenditure for the current month
        days_in_month = today.day
        average_daily_expense = total_expenses / days_in_month if days_in_month > 0 else 0

        return {
            "total_expenses": total_expenses,
            "remaining_balance": remaining_balance,
            "average_daily_expense": average_daily_expense,
        }


class Profile(models.Model):
    """
    Model representing a user's profile.
    Connects to income, expenses, and allows for personal data storage.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="User's current balance.")
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to=get_unique_profile_pic_path, blank=True, null=True,
                                    help_text="User's profile picture.")

    objects = ProfileManager()

    # Add historical records field to track changes
    history = HistoricalRecords()

    def __str__(self):
        """String representation of the profile object, displaying the associated user's username."""
        return f'Profile of {self.user.username}'

    def update_balance(self):
        """
        Update the user's balance.
        The balance is calculated as: income - sum of expenses.
        """
        income = getattr(self.user, 'income', None)
        total_expenses = sum(expense.amount for expense in self.user.expenses.all())
        self.balance = (income.amount if income else 0) - total_expenses
        self.save()

    @property
    def summary(self):
        """Provides a brief summary of the profile, for quick viewing."""
        return f"{self.user}'s balance is {self.balance}"
