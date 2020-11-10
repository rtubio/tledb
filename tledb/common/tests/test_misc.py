
import datetime
import logging
import pytz

from django import test
from unittest import mock

from common import misc

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


class TestMisc(test.SimpleTestCase):

    def setUp(self):

        self._mock_dt_iso = '2020-11-10T10:00:00.000100'
        self._mock_dt_iso_nous = '2020-11-10T10:00:00'
        self._mock_dt_iso_utc = self._mock_dt_iso + '+00:00'
        self._mock_dt_iso_nous_utc = self._mock_dt_iso_nous + '+00:00'

        self._mock_dt = datetime.datetime.fromisoformat(self._mock_dt_iso)
        self._log = logging.getLogger()

    def test_get_utc_timestamp(self):
        """UNIT test: services.common.misc.get_utc_timestamp
        Basic test for the generation of UTC timestamps.
        """
        test_datetime = misc.TIMESTAMP_0 + datetime.timedelta(days=1)
        actual_stamp = misc.get_utc_timestamp(test_datetime)
        expected_stamp = datetime.timedelta(days=1).days * 24 * 3600 * 10**6

        self.assertEqual(expected_stamp, actual_stamp, 'Wrong timestamp!')

    def test_get_fqdn(self):
        """UNIT test: services.common.misc.get_fqdn
        This test validates the function that gets the current hostname.
        """
        self._log.info('>>> test_get_fqdn:')
        hn, ip = misc.get_fqdn_ip()
        self._log.debug('fqdn = ' + str(hn) + ', ip = ' + str(ip))

    def test_get_utc_window(self):
        """UNIT test: services.common.misc.get_utc_window
        """
        self._log.debug('>>> test_get_utc_window:')

        c = misc.get_next_midnight()
        d = datetime.timedelta(minutes=3)

        self.assertEquals(
            misc.get_utc_window(center=c, duration=d), (c - d, c + d)
        )

    @mock.patch('datetime.datetime')
    def test_get_now_hour_utc(self, mock_dt):
        """UNIT test: services.common.misc.get_now_hour_utc
        """
        self._log.debug('>>> test_get_now_hour_utc:')

        mock_dt.utcnow.return_value = self._mock_dt
        expected = datetime.time(hour=10, minute=0, second=0, microsecond=0)
        actual = misc.get_now_hour_utc()
        self.assertEquals(actual, expected, 'Wrong hour returned')

        expected = datetime.time(hour=10, minute=0, second=0, microsecond=100)
        actual = misc.get_now_hour_utc(no_microseconds=False)
        self.assertEquals(actual, expected, 'Wrong hour returned')

    @mock.patch('datetime.datetime')
    def test_get_now_utc(self, mock_dt):
        """UNIT test: services.common.misc.get_now_utc
        """
        self._log.debug('>>> test_get_now_utc:')

        mock_dt.utcnow.return_value = self._mock_dt

        actual = misc.get_now_utc()
        self.assertEquals(actual.isoformat(), self._mock_dt_iso_nous_utc, 'Wrong hour returned')

        actual = misc.get_now_utc(no_microseconds=False)
        self.assertEquals(actual.isoformat(), self._mock_dt_iso_utc, 'Wrong hour returned')
