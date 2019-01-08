
from celery import shared_task

@shared_task
def scrap():
    print('XXXXXXXXXXXXXXX')
