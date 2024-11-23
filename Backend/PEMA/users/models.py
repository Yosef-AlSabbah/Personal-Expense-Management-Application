from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from users.utils import get_unique_profile_pic_path


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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        help_text="User's current balance."
    )
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(
        upload_to=get_unique_profile_pic_path,
        blank=True,
        null=True,
        help_text="User's profile picture."
    )

    objects = ProfileManager()

    # Add historical records field to track changes
    history = HistoricalRecords()

    def __str__(self):
        """String representation of the profile object, displaying the associated user's username."""
        return f'Profile of {self.user}'

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


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True, blank=False,
                                help_text="User's unique username",
                                validators=[
                                    RegexValidator(
                                        regex=r'^[\w-]+$',
                                        message=_(
                                            "Username can only contain letters, numbers, underscores, or hyphens.")
                                    )
                                ]
                                )
    phone_number = models.CharField(_('phone number'), max_length=15, unique=True, null=True, blank=True,
                                    validators=[
                                        RegexValidator(
                                            regex=r'^\+?1?\d{9,15}$',
                                            message=_(
                                                "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
                                            ),
                                        )
                                    ], )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    profile_image = models.ImageField(_('profile image'), upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    last_login_ip = models.GenericIPAddressField(_('last login IP'), null=True, blank=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_manager = models.BooleanField(_('manager status'), default=False)
    is_admin = models.BooleanField(_('admin status'), default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set'  # Avoid clash by adding unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions_set'  # Avoid clash by adding unique related_name
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'first_name', 'last_name']

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username or self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-pk']
