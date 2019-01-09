
from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task


_log = logging.getLogger()


@shared_task
def scrap():
    _log.info('Executing task')
    return('XXXXXXXXXXXXXXX')
