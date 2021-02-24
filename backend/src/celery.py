import os

from celery import Celery


class QueuePriority:
    NORMAL = "normal_priority"


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("Chatroom")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
