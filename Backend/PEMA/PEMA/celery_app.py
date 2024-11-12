from __future__ import absolute_import, unicode_literals

from os import environ

from celery import Celery
from django.conf import settings

environ.setdefault('DJANGO_SETTINGS_MODULE', 'PEMA.settings')

app = Celery('PEMA')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
