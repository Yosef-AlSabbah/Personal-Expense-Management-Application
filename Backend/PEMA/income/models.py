from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Income(models.Model):
    """
    Model representing a user's income entry.
    Each user can only have one income entry.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="income")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of income in the currency unit", default=0)
    date = models.DateField(auto_now_add=True)

    # Automatically updates whenever the instance is saved
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the income object, displaying user, amount, and date."""
        return f'{self.user} received {self.amount} on {self.date}'

    @property
    def summary(self):
        """Provides a brief summary of the income entry, for quick viewing."""
        return f"Income of {self.amount} on {self.date}"

    class Meta:
        # Orders income entries by date, with the most recent first
        ordering = ['-date']

        # Clarifies plural form in the admin panel
        verbose_name_plural = "Incomes"
