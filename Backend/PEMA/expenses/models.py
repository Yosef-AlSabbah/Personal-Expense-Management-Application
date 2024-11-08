from django.contrib.auth import get_user_model

from django.db import models

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


from django.utils import timezone
from collections import defaultdict


class ExpenseManager(models.Manager):
    def for_current_month(self, user):
        """
        Returns all expenses for the given user in the current month.
        """
        now = timezone.now()
        return self.filter(
            user=user,
            date__year=now.year,
            date__month=now.month
        )

    def get_expenses_by_category_for_current_month(self, user):
        """
        Get the expenses of a given user for the current month, grouped by category.
        """
        current_month_expenses = self.for_current_month(user)
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

        # Clarifies plural form in the admin panel
        verbose_name_plural = "Expenses"
