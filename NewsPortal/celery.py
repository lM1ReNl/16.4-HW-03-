import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_mail_every_week': {
        'task': 'news.tasks.weekly_mailing',
        'schedule': crontab(hour=5, minute=0, day_of_week='monday'),
    },
}
app.conf.timezone = 'UTC'

app.autodiscover_tasks()

