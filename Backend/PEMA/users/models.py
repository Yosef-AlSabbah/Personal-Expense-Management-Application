from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
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

#
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError("User must have an email")
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, email, password=None, **extra_fields):
#         user = self.create_user(username, email, password=password, **extra_fields)
#         user.is_active = True
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True)
#     username = models.CharField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#
#     # Set related_name attributes to avoid clashes
#     groups = models.ManyToManyField(
#         Group,
#         related_name="custom_user_groups",
#         blank=True,
#         help_text="The groups this user belongs to.",
#         verbose_name="groups",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="custom_user_permissions",
#         blank=True,
#         help_text="Specific permissions for this user.",
#         verbose_name="user permissions",
#     )
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username", "first_name", "last_name"]
#
#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}"
#
#     def get_short_name(self):
#         return self.username
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     def __str__(self):
#         return self.email
