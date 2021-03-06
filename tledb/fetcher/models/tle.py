"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtpardavila@gmail.com'


import logging
import sys
from urllib.request import urlopen as urllib2_urlopen

from django.core import exceptions, validators
from django.db import models

from common import misc, parse
from fetcher.models.celestrak import CelestrakDatabase as Celestrak


logger = logging.getLogger(__name__)


MAX_TLE_ID_LEN = 24
MAX_TLE_LINE_LEN = 69
REGEX_TLE_LINE = '^[a-zA-Z0-9.\s-]{' + str(MAX_TLE_LINE_LEN) + '}$'


class UpdatedException(Exception):
    """Exception
    Notifies that an object is updated and not created in the database.
    """
    def __init__(self, tleid, reason):
        super().__init__()
        self.tleid = tleid
        self.reason = reason


class CreatedException(Exception):
    """Exception
    Notifies that an object is created in the database.
    """
    def __init__(self, tleid):
        super().__init__()
        self.tleid = tleid


class TLEManager(models.Manager):
    """
    Class that handles all actions related with the TLE database table.
    """

    def create(self, source, l0, l1, l2):
        """
        Overriden create method that adds a new entry in the TLE database
        with the correspondent timestamp about the time of update. The line 0
        of the TLE is used as a identifier for the TLE itself.

        :param source: Link to the source for the TLE
        :param l0: Line #0 of the TLE (identifier)
        :param l1: Line #1 of the TLE
        :param l2: Line #2 of the TLE
        """
        return super(TLEManager, self).create(
            timestamp=misc.get_utc_timestamp(),
            source=source,
            identifier=l0,
            first_line=l1,
            second_line=l2
        )

    def create_or_update(self, source, l0, l1, l2):
        """
        This method creates the new entry in the databse (in case it does not
        exist); otherwise, it updates the existing entry with the given data
        (if necessary).

        :param source: Link to the source for the TLE
        :param l0: Line #0 of the TLE (identifier)
        :param l1: Line #1 of the TLE
        :param l2: Line #2 of the TLE
        """

        l0, l1, l2 = TLEManager.normalize_string(l0, l1, l2)

        try:
            tle = self.get(identifier=l0)
            tle.dirtyUpdate(source=source, identifier=l0, l1=l1, l2=l2)
        except TLE.DoesNotExist as ex:
            logger.info('TLE (%s) does not exist, creating new entry...', l0)
            self.create(source, l0, l1, l2)

    @staticmethod
    def normalize_string(l0, l1, l2):
        """Static method
        Normalizes the three parameters from unicode to string, in case it is
        necessary.
        :param l0: Line#0 of the TLE file
        :param l1: Line#1 of the TLE file
        :param l2: Line#2 of the TLE file
        :return: Tuple (l0, l1, l2)
        """

        if isinstance(l0, bytes):
            l0 = l0.decode('utf-8')
        if isinstance(l1, bytes):
            l1 = l1.decode('utf-8')
        if isinstance(l2, bytes):
            l2 = l2.decode('utf-8')

        return l0, l1, l2

    @staticmethod
    def load_celestrak():
        """
        Loads the TLE from all the accessible resources from celestrak.com
        """
        read = 0
        loaded = 0
        updated = 0
        erroneous = 0

        for s_tuple in Celestrak.CELESTRAK_SECTIONS:

            section = s_tuple[0]
            tle_info = s_tuple[1]

            for (url, description) in tle_info:
                r, l, u, e = TLEManager.load_tles(source=url)

                read += r
                loaded += l
                updated += u
                erroneous += e

        return read, loaded, updated, erroneous

    @staticmethod
    def load_tles(source=Celestrak.CELESTRAK_CUBESATS, testing=False):
        """
        This method loads the TLE's in the database and updates them in
        accordance with the latest information gathered from NORAD's website.

        :param source: URL to the file with the TLE's
        :param testing: Flag that indicates an internal testing state
        :returns: tuple with the number of TLE objects loaded and erroneous
        """
        read = 0
        loaded = 0
        updated = 0
        erroneous = 0

        l_n = 0
        l0, l1, l2 = '', '', ''

        for l_i in urllib2_urlopen(source):

            if l_n % 3 == 0:
                l0 = l_i.rstrip()
                l_n += 1
                continue

            if l_n % 3 == 1:
                l1 = l_i.rstrip()
                l_n += 1
                continue

            if l_n % 3 == 2:
                l2 = l_i.rstrip()
                l_n += 1

            try:
                read += 1
                TLE.objects.create_or_update(
                    source=source, l0=l0, l1=l1, l2=l2
                )
            except CreatedException as ex:
                logger.info('TLE %s has been created', ex.tleid)
                loaded += 1
            except UpdatedException as ex:
                logger.info('TLE %s updated, reason = %s', ex.tleid, ex.reason)
                updated += 1
            except ValueError as ex:
                logger.warn('Error reading TLE = ' + str(l0))
                erroneous += 1

        return read, loaded, updated, erroneous


class TLE(models.Model):
    """TLE database model.
    Class that models the TLE elements within the database.
    """
    class Meta:
        app_label = 'fetcher'
        ordering = ['identifier']

    objects = TLEManager()

    identifier = models.CharField(
        'Spacecraft', max_length=MAX_TLE_ID_LEN, unique=True
    )

    timestamp = models.BigIntegerField('Timestamp')

    source = models.TextField(
        'Source',
        max_length=100,
        validators=[validators.URLValidator()]
    )

    first_line = models.CharField(
        'L1',
        max_length=MAX_TLE_LINE_LEN,
        validators=[
            validators.RegexValidator(
                regex=REGEX_TLE_LINE,
                message="Alphanumeric or '.-_' required",
                code='invalid_tle_line_1'
            )
        ]
    )

    second_line = models.CharField(
        'L2',
        max_length=MAX_TLE_LINE_LEN,
        validators=[
            validators.RegexValidator(
                regex=REGEX_TLE_LINE,
                message="Alphanumeric or '.-_' required",
                code='invalid_tle_line_2'
            )
        ]
    )

    def dirtyUpdate(self, source, identifier, l1, l2):
        """
        Updates the configuration for this TwoLineEelment with the data
        provided.
        :param source: The source for this TLE.
        :param identifier: The identification line of the TLE (line #0).
        :param l1: The first line of the TLE (line#1).
        :param l2: The second line of the TLE (line#2).
        """
        changed = False
        reason = None

        if self.identifier != identifier:
            reason = 'identifier ({}, {})'.format(self.identifier, identifier)
            self.identifier = identifier
            changed = True

        if self.first_line != l1:
            reason = 'l1: ({}, {})'.format(self.first_line, l1)
            self.first_line = l1
            changed = True

        if self.second_line != l2:
            reason = 'l2: ({}, {})'.format(self.second_line, l2)
            self.second_line = l2
            changed = True

        if self.source != source:
            logger.debug('Multiple appearance for %s', identifier)
            self.source = source

        if changed:
            self.timestamp = misc.get_utc_timestamp()
            self.save()
            raise UpdatedException(self.identifier, reason)
