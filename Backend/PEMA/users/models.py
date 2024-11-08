from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    """
    Model representing a user's profile.
    Connects to income, expenses, and allows for personal data storage.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="User's current balance.")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the profile object, displaying the associated user's username."""
        return f'Profile of {self.user.name}'

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
