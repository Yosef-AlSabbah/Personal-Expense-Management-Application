from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Income

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_income(sender, instance, created, **kwargs):
    """Automatically create an Income entry for every new user."""
    if created:
        Income.objects.create(user=instance, amount=0.00, description="Default income")
