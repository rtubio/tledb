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


logger = logging.getLogger('configuration')


MAX_TLE_ID_LEN = 24
MAX_TLE_LINE_LEN = 69


class TLEChecker(object):
    """
    Class that models a single TLE object, stripping its 3 line contents into
    several fields.
    """

    def check(self):
        """
        This method checks that the fields of the TLE object are coherent.
        """
        assert self.l1_satellite_number == self.l2_satellite_number
        assert len(self.l0) <= MAX_TLE_ID_LEN
        assert len(self.l1) <= MAX_TLE_LINE_LEN
        assert len(self.l2) <= MAX_TLE_LINE_LEN

    def readFields(self):
        """
        This method reads the fields for the TLE object from within the TLE
        string lines.
        """

        self.l0_satellite_name = self.l0
        self.l1_satellite_number_w_classification = self.l1[2:7].strip()
        self.l1_satellite_number = int(self.l1[2:6].strip())
        self.l1_satellite_classification = self.l1[7:8].strip()
        self.l1_international_designator_launch_yr = int(self.l1[9:11].strip())
        self.l1_international_designator_launch_no = int(self.l1[11:14].strip())
        self.l1_international_designator_launch_piece = self.l1[14:17].strip()
        self.l1_epoch_year = int(self.l1[18:20].strip())
        self.l1_epoch_day_fraction = float(self.l1[20:32].strip())
        self.l1_1st_d_mean_motion = float(self.l1[33:43].strip())

        self.l1_2nd_d_mean_motion = parse.tle_scientific_2_float(
            self.l1[44:52]
        )

        self.l1_bstar = parse.tle_scientific_2_float(self.l1[53:61].strip())
        self.l1_set_no = int(self.l1[64:68].strip())
        self.l1_checksum = int(self.l1[68:69].strip())

        self.l2_satellite_number = int(self.l2[2:8].strip())
        self.l2_inclination_deg = float(self.l2[8:16].strip())
        self.l2_raan_deg = float(self.l2[17:25].strip())
        self.l2_eccentricity = float(self.l2[26:33].strip())
        self.l2_arg_perigee_deg = float(self.l2[34:42].strip())
        self.l2_mean_anomaly_deg = float(self.l2[43:51].strip())
        self.l2_mean_motion_revs = float(self.l2[52:63].strip())
        self.l2_revolution_no = int(self.l2[63:68].strip())
        self.l2_checksum = int(self.l2[68].strip())

    def __init__(self, l0, l1, l2):
        """Main Constructor
        Builds the TLE object using the given parameters.
        """
        self.l0 = l0
        self.l1 = l1
        self.l2 = l2

        self.readFields()
        self.check()

    def __str__(self):
        """stringifier"""
        return self.l0_satellite_name + '\n' +\
                self.l1_satellite_number_w_classification


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
        TLEManager.check_tle_format(l0, l1, l2)

        return super(TLEManager, self).create(
            timestamp=misc.get_utc_timestamp(),
            source=source,
            identifier=l0,
            first_line=l1,
            second_line=l2,
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
        :return: a reference to the newly created object in the databse.
        """
        try:
            tle = self.get(identifier=l0)
            return tle.dirtyUpdate(source=source, identifier=l0, l1=l1, l2=l2)
        except:
            logger.info('l1[%d] = %s', len(l1), l1)
            return self.create(source, l0, l1, l2)

    @staticmethod
    def normalize_string(l0, l1, l2):
        """Static method
        Normalizes the three parameters from unicode to string, in case it is
        necessary.
        :param l0: Line#0 of the TLE file
        :param l1: Line#1 of the TLE file
        :param l2: Line#2 of the TLE file
        :return: Tuple (l0, l1, l2)

        OLD encoding change from str to 'ascii', Python 2.7
        if isinstance(l0, str):
            l0 = unicodedata.normalize('NFKD', l0).encode('ascii', 'ignore')
        if isinstance(l1, str):
            l1 = unicodedata.normalize('NFKD', l1).encode('ascii', 'ignore')
        if isinstance(l2, str):
            l2 = unicodedata.normalize('NFKD', l2).encode('ascii', 'ignore')
        """

        if isinstance(l0, bytes):
            l0 = str(l0, 'ascii')
        if isinstance(l1, bytes):
            l1 = str(l1, 'ascii')
        if isinstance(l2, bytes):
            l2 = str(l2, 'ascii')

        return l0, l1, l2

    @staticmethod
    def check_tle_format(l0, l1, l2):
        """Static method
        Checks whether the format for a given TLE is correct or not.
        :param l0: Line#0 of the TLE file
        :param l1: Line#1 of the TLE file
        :param l2: Line#2 of the TLE file
        :return: True if the operation could succesuffly be completed
        """
        l0, l1, l2 = TLEManager.normalize_string(l0, l1, l2)
        try:
            TLEChecker(l0, l1, l2)
        except AssertionError as err:
            logger.warn('Error parsing (%s, %s, %s), ex = %s', l0, l1, l2, err)

        return True

    @staticmethod
    def load_celestrak():
        """
        Loads the TLE from all the accessible resources from celestrak.com
        """
        for s_tuple in Celestrak.CELESTRAK_SECTIONS:

            logger.info('*')

            section = s_tuple[0]
            tle_info = s_tuple[1]

            for (url, description) in tle_info:
                logger.info('.')
                TLEManager.load_tles(source=url)

    @staticmethod
    def load_tles(source=Celestrak.CELESTRAK_CUBESATS, testing=False):
        """
        This method loads the TLE's in the database and updates them in
        accordance with the latest information gathered from NORAD's website.

        :param source: URL to the file with the TLE's
        :param testing: Flag that indicates an internal testing state
        """
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
                TLE.objects.create_or_update(
                    source=source, l0=l0, l1=l1, l2=l2
                )
            except ValueError as ex:
                if testing:
                    logger.warn('Error reading TLE = ' + str(l0))
                    continue
                else:
                    raise ex


class TLE(models.Model):
    """TLE database model.
    Class that models the TLE elements within the database.
    """
    class Meta:
        app_label = 'fetcher'
        ordering = ['identifier']

    objects = TLEManager()

    identifier = models.CharField(
        'Identifier of the spacecraft that this TLE element models (line 0)',
        max_length=24,
        unique=True
    )

    timestamp = models.BigIntegerField(
        'Timestamp with the update date for this TLE'
    )

    source = models.TextField(
        'String that indicates the source of this TLE',
        max_length=100,
        validators=[validators.URLValidator()]
    )

    first_line = models.CharField(
        'First line of this TLE',
        max_length=MAX_TLE_LINE_LEN,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\s-]{69}$',
                message="Alphanumeric or '.-_' required",
                code='invalid_tle_line_1'
            )
        ]
    )
    second_line = models.CharField(
        'Second line of this TLE',
        max_length=MAX_TLE_LINE_LEN,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\s-]{69}$',
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
        changed_flag = False

        if self.identifier != identifier:
            self.identifier = identifier
            changed_flag = True

        if self.first_line != l1:
            self.first_line = l1
            changed_flag = True

        if self.second_line != l2:
            self.second_line = l2
            changed_flag = True

        if self.source != source:
            self.source = source
            changed_flag = True

        if changed_flag:
            self.timestamp = misc.get_utc_timestamp()
            self.save()

        return self
