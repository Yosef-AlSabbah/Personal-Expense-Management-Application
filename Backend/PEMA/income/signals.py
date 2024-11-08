from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from income.models import Income

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_income(sender, instance, created, **kwargs):
    """
    Signal to create a Profile whenever a new User is created.
    """
    if created:
        Income.objects.create(user=instance)
