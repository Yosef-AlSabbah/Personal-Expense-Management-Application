from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def update_user_balances():
    """
    Task to update the balance of each user's profile by adding their monthly income.
    This task is intended to be run at the start of each month.
    """
    users = User.objects.all()
    for user in users:
        # Add the monthly income to the user's current balance
        user.profile.balance += user.income.amount

        # Save the updated balance back to the database
        user.profile.save()
