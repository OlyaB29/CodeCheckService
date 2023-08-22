from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

from .settings import INSTALLED_APPS


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_check_service.settings')


app = Celery("code_check_service")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: INSTALLED_APPS)

app.conf.beat_schedule = {
    # Запуск проверки новых файлов будет осуществляться каждые 5 минут
    'every_5_minutes_new_files_check': {
        'task': 'check_app.tasks.run_files_check',
        'schedule': crontab(minute="*/5"),
    },
}
