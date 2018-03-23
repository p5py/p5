"""This module manages the Time and Date functions of p5py"""

import datetime


def day():
    """Day (1-31)
        :returns: The current day of the month
        :rtype: int"""
    dt = datetime.datetime.now()
    return dt.day


def month():
    """Month (1-12)
        :returns: The current month of the year
        :rtype: int"""
    dt = datetime.datetime.now()
    return dt.month


def year():
    """Year (1-9999)
        :returns: The current year
        :rtype: int"""
    dt = datetime.datetime.now()
    return dt.year


def second():
    """Second (0-59)
        :returns: The current second
        :rtype: int"""
    dt = datetime.datetime.now()
    return dt.second


def minute():
    """Minute (0-59)
        :returns: The current minute
        :rtype: int"""
    dt = datetime.datetime.now()
    return dt.minute


def hour():
    """Hour (0-23)
        :returns: The current hour
        :rtype: int"""
    dt = datetime.datetime.now()
    return dt.hour


def milli_seconds():
    """Milliseconds
        :returns: The time in milliseconds since the epoch
        :rtype: int"""
    import time
    return int(round(time.time()*1000))


def millis():
    """Millis (0-......)
        :returns: The time in milliseconds since starting the program
        :rtype: int"""
    from .base import start_time
    return milli_seconds() - start_time
