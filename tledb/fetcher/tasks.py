
from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task

from fetcher.models import tle


_log = logging.getLogger(__name__)


@shared_task
def scrap():

    _log.info('Scrapping Celestrak database...')
    r, l, u, e = tle.TLEManager.load_celestrak()
    result = "read: {}, load: {}, updated: {}, errors: {}".format(r, l, u, e)
    _log.info(result)
    _log.info('Scrapping done!')
    return result
