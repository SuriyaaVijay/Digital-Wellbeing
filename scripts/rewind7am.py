#!/usr/bin/env python3

""" rewind7am.py for uLogMe:

Usage:
$ rewind7am.py

Simple utility script that takes unix time (as int)
and returns unix time at 7am of the day that the corresponding ulogme
event belongs to. ulogme day breaks occur at 7am, so e.g. 3am late
night session will count towards previous day activity

Note: works in both Python 2 and 3.
"""
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

import sys
import datetime
import time


def ppDay(t):
    """
    Print the time as a the date of the day, and not a unix time.
    """
    d = datetime.datetime.fromtimestamp(t)
    return d.strftime("%A %d %B %Y")


def ppTime(t):
    """
    Print the time as a the date and hour, and not a unix time.
    """
    d = datetime.datetime.fromtimestamp(t)
    return d.strftime("%A %d %B %Y, %r")


def rewindTime(t):
    """
    Simple utility function that takes unix time (as int)
    and returns unix time at 7am of the day that the corresponding ulogme
    event belongs to. ulogme day breaks occur at 7am, so e.g. 3am late
    night session will count towards previous day activity
    """
    d = datetime.datetime.fromtimestamp(t)
    if d.hour >= 7:
        # it's between 7am-11:59pm
        d = datetime.datetime(d.year, d.month, d.day, 7)  # rewind time to 7am
    else:
        # it's between 12am-7am, so this event still belongs to previous day
        d = datetime.datetime(d.year, d.month, d.day, 7)  # rewind time to 7am
        d -= datetime.timedelta(days=1)  # subtract a day

    curtime = int(d.strftime("%s"))
    return curtime


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        # no argument given? use right now
        print(rewindTime(int(time.time())))
    else:
        print(rewindTime(int(sys.argv[1])))
