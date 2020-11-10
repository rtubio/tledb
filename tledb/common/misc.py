
import datetime
import logging
import pytz
import socket


logger = logging.getLogger('common')


def get_fqdn(ip_address):
    """
    Function that transforms a given IP address into the associated FQDN name
    for that host.
    :param ip_address: IP address of the remote host.
    :return: FQDN name for that host.
    """
    return socket.gethostbyaddr(ip_address)


# noinspection PyBroadException
def get_fqdn_ip():
    """
    Function that returns the hostname as read from the socket library and
    the IP address for that hostname.
    :return: (String with the name of the current host, IP)
    """
    hn = 'localhost'
    try:
        hn = socket.getfqdn()
    except Exception:
        pass

    return hn, socket.gethostbyname(hn)


def get_now_utc(no_microseconds=True):
    """
    This method returns now's datetime object UTC localized.
    :param no_microseconds: sets whether microseconds should be cleared.
    :return: the just created datetime object with today's date.
    """
    if no_microseconds:
        return pytz.utc.localize(datetime.datetime.utcnow()).replace(
            microsecond=0
        )
    else:
        return pytz.utc.localize(datetime.datetime.utcnow())


def get_utc_window(center=None, duration=None, no_microseconds=True):
    """X minutes window
    Function that returns a time window (start, end tuple) centered at the
    current instant and with a length of as many minutes as specified as a
    parameter. By default, the lenght is 10 minutes and the center of the
    window is the execution instant.

    Args:
        center: datetime.datetime object that defines the center of the window
        duration: datetime.timedelta object with the duration of the window
        no_microseconds: flag that indicates whether the microseconds should
                            be included in the window tuple or not
    Returns: (start, end) tuple that defines the window
    """
    if not center:
        center = get_now_utc(no_microseconds=no_microseconds)
    if not duration:
        duration = datetime.timedelta(minutes=5)

    return center - duration, center + duration


def get_now_hour_utc(no_microseconds=True):
    """
    This method returns now's hour in the UTC timezone.
    :param no_microseconds: sets whether microseconds should be cleared.
    :return: The time object within the UTC timezone.
    """
    if no_microseconds:
        return datetime.datetime.utcnow().replace(microsecond=0).time()
    else:
        return datetime.datetime.utcnow().time()


def get_today_utc():
    """
    This method returns today's date localized with the microseconds set to
    zero.
    :return: the just created datetime object with today's date.
    """
    return pytz.utc.localize(datetime.datetime.utcnow()).replace(
        hour=0, minute=0, second=0, microsecond=0
    )


def get_next_midnight():
    """
    This method returns today's datetime 00am.
    :return: the just created datetime object with today's datetime 00am.
    TODO :: unit test
    """
    return pytz.utc.localize(datetime.datetime.today()).replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + datetime.timedelta(days=1)


def localize_date_utc(date):
    """
    Localizes in the UTC timezone the given date object.
    :param date: The date object to be localized.
    :return: A localized datetime object in the UTC timezone.
    TODO :: unit test
    """
    return pytz.utc.localize(
        datetime.datetime.combine(
            date, datetime.time(hour=0, minute=0, second=0)
        )
    )


TIMESTAMP_0 = localize_date_utc(datetime.datetime(year=1970, month=1, day=1))


def get_utc_timestamp(utc_datetime=None):
    """
    Returns a timestamp with the number of microseconds ellapsed since January
    1st of 1970 for the given datetime object, UTC localized.
    :param utc_datetime: The datetime whose timestamp is to be calculated.
    :return: The number of miliseconds since 1.1.1970, UTC localized (integer)
    """
    if utc_datetime is None:
        utc_datetime = get_now_utc()
    diff = utc_datetime - TIMESTAMP_0
    return int(diff.total_seconds() * 10**6)
