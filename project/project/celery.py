import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Be sure that this task is imported
from health_check.contrib.celery.tasks import add


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
