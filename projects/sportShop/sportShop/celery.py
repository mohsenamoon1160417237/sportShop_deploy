import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'sportShop.settings')
app = Celery('sportShop')

app.config_from_object('django.conf:settings' , namespace='CELERY')


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')


app.conf.beat_schedule = {
    #Scheduler Name
    'refresh-access-token': {
        # Task Name (Name Specified in Decorator)
        'task': 'manageProduct.tasks.refreshAccessToken',
        # Schedule
        'schedule': crontab(minute='*/1')
        #'schedule': crontab(minute=0,
        #                    hour=1,
        #                    day_of_week='sunday'),
        # Function Arguments
    },
    #Scheduler Name
    'upload-product-instagram': {
        # Task Name (Name Specified in Decorator)
        'task': 'manageProduct.tasks.postInsta',
        # Schedule
        'schedule': crontab(minute='*/1'),
        #'schedule': crontab(minute=0,
        #                    hour='5'),
    }
}
