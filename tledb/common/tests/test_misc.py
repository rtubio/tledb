
import datetime
import logging
import pytz

from django import test

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
