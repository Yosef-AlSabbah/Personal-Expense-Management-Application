from django.apps import AppConfig
from django.contrib.auth import get_user_model
from simple_history import register


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        User = get_user_model()

        # Add historical records field to track changes
        register(User)
