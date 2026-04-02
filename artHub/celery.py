import multiprocessing
import os
import django
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'artHub.settings'
)

app = Celery('artHub')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# if __name__ == "__main__":
#     multiprocessing.freeze_support()
#     from django.core.management import execute_from_command_line
#     execute_from_command_line()