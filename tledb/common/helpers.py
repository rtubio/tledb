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
__author__ = 'rtubiopa@calpoly.edu'

import base64
import datetime

from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.test.client import RequestFactory

from services.accounts.models import UserProfile
from services.common import misc, gis
from services.communications import models as comms_models
from services.configuration.models import bands, channels, segments, tle
from services.configuration.jrpc.serializers import rules
from services.leop.models import launch as leop_models
from services.network.models import server as server_models


def create_user(
    username='testuser', password='testuser.', email='test@test.test'
):
    user = User.objects.create_user(
        username=username, email=email, password=password
    )
    user.save()
    return user


def create_user_profile(
    username='testuser', password='testuser.',
    email='test@test.test', is_staff=False
):

    first_name, last_name = 'test_first_name', 'test_last_name'
    organization, country = 'test_organization', 'US'

    with transaction.atomic():
        user_profile = UserProfile.objects.create(
            username=username,
            first_name=first_name, last_name=last_name,
            email=email,
            organization=organization, country=country,
            is_active=False, is_verified=False, blocked=False,
            is_staff=is_staff
        )

    user_id = user_profile.user_ptr_id
    new_user = User.objects.get(id=user_id)
    new_user.set_password(password)
    new_user.save()

    return user_profile


def create_request(url='/test', user_profile=None, user_ip='129.65.71.110'):

    factory = RequestFactory()
    request = factory.get(url)

    request.META['REMOTE_ADDR'] = user_ip

    if user_profile:
        request.user = user_profile
    else:
        request.user = create_user_profile()

    return request


def create_sc(
    user_profile=None,
    identifier='sc-uvigo',
    callsign='BABA00',
    tle_id='HUMSAT-D',
    is_ufo=False
):

    username = 'testuser'

    try:
        if not user_profile:
            user_profile = create_user_profile(username=username)
    except IntegrityError:
        user_profile = UserProfile.objects.get(username=username)

    return segments.Spacecraft.objects.create(
        user=user_profile,
        identifier=identifier,
        callsign=callsign,
        tle_id=tle_id,
        is_ufo=is_ufo
    )


MESSAGE__1_TEST = 'QWxhZGRpbjpvcGVuIHNlc2FtZQ=='
MESSAGE__2_TEST = 'ogAAAABErEarAAAAAESsRwoAAAAARKxHaAAAAABErEfGAA' \
                  'AAAESsSCVCE4y4RKxIg0NICpdErEjhQ4IvIkSsSUBDKx7d' \
                  'RKxJngAAAABErEn8AAAAAESsSloAAAAARKxKuQAAAABEtQ' \
                  'kRAAAAAES1CXkAAAAARLUJ4QAAAABEtQpKAAAAAES1CrJD' \
                  'JhD9RLULGkN2IZtEtQuCQ0j6M0S1C'

"""
MESSAGE_BASE64 = b'Base64 is a group of similar binary-to-text encoding ' \
                 b'schemes that represent binary data in an ASCII string ' \
                 b'format '\
                 b'by translating it into a radix-64 representation. The term '\
                 b'Base64 '\
                 b'originates from a specific MIME content transfer encoding.'
"""

MESSAGE_BASE64 = base64.b64encode(bytes(
    'Base64 is a group of similar binary-to-text encoding schemes that '
    'represent binary data in an ASCII string format by translating it into a '
    'radix-64 representation. The term Base64 originates from a specific MIME '
    'content transfer encoding.',
    'UTF-8'
))


def create_message(groundstation, message=MESSAGE__1_TEST):

    server_dt = misc.get_now_utc()
    server_ts = misc.get_utc_timestamp(server_dt)
    gs_dt = server_dt - datetime.timedelta(hours=2)
    gs_ts = misc.get_utc_timestamp(gs_dt)

    return comms_models.PassiveMessage.objects.create(
        groundstation=groundstation,
        doppler_shift=0.0,
        groundstation_timestamp=gs_ts,
        reception_timestamp=server_ts,
        message=message
    )


def create_local_server():

    server_models.Server.objects.load_local_server()

ISS_TLE_ID = 'ISS (ZARYA)'
ISS_TLE = [
    '1 25544U 98067A   16007.60119943  .00006067  00000-0  94765-4 0  9991',
    '2 25544  51.6421 143.8872 0008530  12.1082  99.2147 15.55287271979846'
]

TIANGONG_TLE = [
    '1 37820U 11053A   16007.38899255  .00011184  00000-0  15007-3 0  9994',
    '2 37820  42.7634 131.4885 0009376   9.5630  49.9906 15.57917653245306'
]


def create_launch(
    username='admin-cluster-1',
    admin=None,
    identifier='cluster-1',
    tle_l1=ISS_TLE[0],
    tle_l2=ISS_TLE[1],
    date=None
):

    try:
        if not admin:
            admin = create_user_profile(username=username)
    except IntegrityError:
        admin = UserProfile.objects.get(username=username)

    if not date:
        date = datetime.datetime.today()

    return leop_models.Launch.objects.create(
        admin, identifier, date, tle_l1, tle_l2
    )


def init_available():

    o = bands.AvailableModulations.objects.create(modulation='FM')
    o.save()
    o = bands.AvailableModulations.objects.create(modulation='AFSK')
    o.save()
    o = bands.AvailableBitrates.objects.create(bitrate=300)
    o.save()
    o = bands.AvailableBitrates.objects.create(bitrate=600)
    o.save()
    o = bands.AvailableBitrates.objects.create(bitrate=900)
    o.save()
    o = bands.AvailableBandwidths.objects.create(bandwidth=12.500)
    o.save()
    o = bands.AvailableBandwidths.objects.create(bandwidth=25.000)
    o.save()
    o = bands.AvailablePolarizations.objects.create(polarization='LHCP')
    o.save()
    o = bands.AvailablePolarizations.objects.create(polarization='RHCP')
    o.save()


def init_tles_database():
    """
    Loads only the TLE's for the CubeSat section from celestrak.com.
    """
    tle.TwoLineElementsManager.load_celestrak()


def create_band(minimum_frequency=435000000, maximum_frequency=438000000):

    return bands.AvailableBands.objects.create(
        IARU_range='UHF',
        IARU_band='70 cm',
        AMSAT_letter='U',
        IARU_allocation_minimum_frequency=minimum_frequency,
        IARU_allocation_maximum_frequency=maximum_frequency,
        uplink=True,
        downlink=True
    )


def create_gs(
    user_profile=None,
    identifier='gs-castrelos',
    callsign='KAKA00',
    contact_elevation=10,
    latitude=33.9333,
    longitude=-118.3880,
    altitude=20,
):

    if not user_profile:
        user_profile = create_user_profile()

    if altitude is None:
        altitude = gis.get_altitude(latitude, longitude)

    return segments.GroundStation.objects.create(
        user=user_profile,
        identifier=identifier,
        callsign=callsign,
        contact_elevation=contact_elevation,
        longitude=longitude,
        latitude=latitude,
        altitude=altitude
    )


def sc_add_channel(
    sc,
    frequency,
    channel_id,
    modulation=None,
    bitrate=None,
    bandwidth=None,
    polarization=None
):

    if not modulation:
        modulation = bands.AvailableModulations.objects.all()[0]
    if not bitrate:
        bitrate = bands.AvailableBitrates.objects.all()[0]
    if not bandwidth:
        bandwidth = bands.AvailableBandwidths.objects.all()[0]
    if not polarization:
        polarization = bands.AvailablePolarizations.objects.get(
            polarization='RHCP'
        )

    return channels.SpacecraftChannel.objects.create(
        spacecraft=sc,
        identifier=channel_id,
        frequency=frequency,
        modulation=modulation,
        bitrate=bitrate,
        bandwidth=bandwidth,
        polarization=polarization
    )


def remove_sc(spacecraft_id):

    segments.Spacecraft.objects.get(identifier=spacecraft_id).delete()


def remove_sc_channel(sc_ch_id):

    channels.SpacecraftChannel.objects.get(identifier=sc_ch_id).delete()


def gs_add_channel(
    gs, band, gs_ch_id,
    modulations=None, bitrates=None, bandwidths=None, polarizations=None
):

    if modulations is None:
        modulations = bands.AvailableModulations.objects.all()
    if bitrates is None:
        bitrates = bands.AvailableBitrates.objects.all()
    if bandwidths is None:
        bandwidths = bands.AvailableBandwidths.objects.all()
    if polarizations is None:
        polarizations = bands.AvailablePolarizations.objects.all()

    return channels.GroundStationChannel.objects.create(
        groundstation=gs,
        identifier=gs_ch_id,
        band=band,
        modulations=modulations,
        bitrates=bitrates,
        bandwidths=bandwidths,
        polarizations=polarizations
    )


def remove_gs_channel(gs_id, gs_ch_id):

    return channels.GroundStationChannel.objects.get(
        identifier=gs_ch_id, groundstation__identifier=gs_id
    ).delete()


def create_jrpc_once_rule(
    operation=rules.RULE_OP_ADD, starting_time=None, ending_time=None
):

    now = misc.get_now_utc()

    if starting_time is None:
        starting_time = now + datetime.timedelta(minutes=30)
    if ending_time is None:
        ending_time = now + datetime.timedelta(minutes=45)

    return {
        rules.RULE_OP: operation,
        rules.RULE_PERIODICITY: rules.RULE_PERIODICITY_ONCE,
        rules.RULE_DATES: {
            rules.RULE_ONCE_S_TIME: starting_time.isoformat(),
            rules.RULE_ONCE_E_TIME: ending_time.isoformat()
        },
    }


def create_jrpc_daily_rule(
    operation=rules.RULE_OP_ADD,
    date_i=None, date_f=None,
    starting_time=None, ending_time=None
):

    if date_i is None:
        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
    if date_f is None:
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)

    now = misc.get_now_utc()

    if starting_time is None:
        starting_time = now + datetime.timedelta(minutes=30)
    if ending_time is None:
        ending_time = now + datetime.timedelta(minutes=45)

    return {
        rules.RULE_OP: operation,
        rules.RULE_PERIODICITY: rules.RULE_PERIODICITY_DAILY,
        rules.RULE_DATES: {
            rules.RULE_DAILY_I_DATE: date_i.isoformat(),
            rules.RULE_DAILY_F_DATE: date_f.isoformat(),
            rules.RULE_S_TIME: starting_time.isoformat(),
            rules.RULE_E_TIME: ending_time.isoformat()
        },
    }


def create_identifier_list(json_slot_list):
    identifier_l = []

    for l_i in json_slot_list:

        identifier_l.append(l_i['identifier'])

    return identifier_l
