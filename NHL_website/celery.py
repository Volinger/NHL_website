import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NHL_website.settings')

app = Celery('NHL_Database')

# app.conf.broker_url = 'redis://localhost:5674/0'
# app.conf.result_backend = 'redis://localhost:5674/0'

app.conf.broker_url = 'redis://redis-broker.azurewebsites.net'
app.conf.result_backend = 'redis://redis-broker.azurewebsites.net'

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
