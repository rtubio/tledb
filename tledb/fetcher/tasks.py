
from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task

from fetcher.models import tle


_log = logging.getLogger()


@shared_task
def scrap():

    _log.info('Scrapping Celestrak database')
    tle.TLEManager.load_celestrak()
