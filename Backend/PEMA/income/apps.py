from django.apps import AppConfig


class IncomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'income'

    def ready(self):
        import income.signals
