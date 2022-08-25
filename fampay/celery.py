"""Celery Configuration file"""

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "fampay.settings")

app = Celery("fampay", broker=settings.CELERY_BROKER, backend=settings.CELERY_BROKER)

app.config_from_object("django.conf.settings", namespace="CELERY")

app.autodiscover_tasks()
