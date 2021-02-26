import pytest
from django.conf import settings


@pytest.fixture()
def celery_task_eager():
    settings.CELERY_TASK_ALWAYS_EAGER = True
