from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """
    Model representing a category for expenses, such as 'Food', 'Transport', etc.
    Each category has a name and an optional description.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """String representation of the category object, displaying the category name."""
        return self.name

    @property
    def title(self):
        """Return the name of the category as its title."""
        return self.name

    class Meta:
        # Clarifies plural form in the admin panel
        verbose_name_plural = "Categories"


class ExpenseManager(models.Manager):
    def get_expenses_for_current_month(self, user):
        """
        Retrieves all expenses for the current month for a specified user.
        Filters expenses by the authenticated user and the current year and month.
        """
        now = timezone.now()
        return self.filter(
            user=user,
            date__year=now.year,
            date__month=now.month
        )

    def get_expenses_by_category_for_current_month(self, user=None):
        """
        Retrieves and groups expenses by category for the current month for a specified user.
        This groups each expense by its category, creating a dictionary with category keys
        and lists of expense instances as values.
        """
        current_month_expenses = self.get_expenses_for_current_month(user)
        expenses_by_category = defaultdict(list)

        for expense in current_month_expenses:
            expenses_by_category[expense.category].append(expense)

        return expenses_by_category


class Expense(models.Model):
    """
    Model representing an expense, associated with a user, amount, date, and a category.
    Each expense can have an optional description.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount spent in the currency unit")
    date = models.DateField(auto_now_add=True)  # Automatically sets the date to the creation date
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="expenses"
    )
    description = models.TextField(blank=True, null=True)

    objects = ExpenseManager()  # Adding the custom manager here

    def __str__(self):
        """String representation of the expense object, displaying user, amount, and date."""
        return f'{self.user} spent {self.amount} on {self.date}'

    @property
    def summary(self):
        """Provides a brief summary of the expense, for quick viewing."""
        return f"Expense of {self.amount} in {self.category}"

    class Meta:
        # Orders expenses by date, with the most recent first
        ordering = ['-date']
        verbose_name_plural = "Expenses"
