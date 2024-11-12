import json

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule


class Command(BaseCommand):
    help = "Sets up a monthly periodic task for updating user balances"

    def handle(self, *args, **kwargs):
        # Define the schedule: midnight on the 1st of each month
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_month="1",
            month_of_year="*",
        )

        # Create or update the periodic task
        task, created = PeriodicTask.objects.update_or_create(
            crontab=schedule,
            name="Monthly update of user balances",
            task="income.tasks.update_user_balances",
            defaults={"args": json.dumps([])},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Monthly task created successfully"))
        else:
            self.stdout.write(self.style.SUCCESS("Monthly task updated successfully"))

