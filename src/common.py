#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-03-12
#

"""
"""

from __future__ import print_function, unicode_literals

from datetime import date, timedelta
import locale
import logging
import re

from workflow import Workflow
from workflow.util import run_command


log = logging.getLogger(__name__)


# Regex for parsing a locale from date formats
LANG_SEARCH = re.compile(r"""LANG=([a-z]{2}(?:_[A-Z]{2})?)""",
                         re.IGNORECASE).search

# Regex for parsing user input
QUERY_MATCH = re.compile(r"""([+-]{0,1})(\d+)([d|w|y]{0,1})""",
                         re.IGNORECASE).match


# Generic defaults
FALLBACK_DATE_FORMATS = [
    '%x',
    '%Y-%m-%d',
    '%d %b %Y',
    '%d %B %Y',
]

# Locale-specific defaults
DEFAULT_DATE_FORMATS = {
    'en_GB': [
        '%x',
        '%Y-%m-%d',
        '%d %b. %Y',
        '%d %B %Y',
        '%d %b. %Y',
        '%d %B %Y',
    ],
    'en_US': [
        '%x',
        '%Y-%m-%d',
        '%b. %d %Y',
        '%B %d %Y',
        '%b. %d %Y',
        '%B %d %Y',
    ],
    'de_DE': [
        '%x',
        '%Y-%m-%d',
        '%d. %b. %Y',
        '%d. %B %Y',
        '%d. %b. %Y',
        '%d. %B %Y',
    ],
}


class DateError(Exception):
    """Base exception class."""


class InvalidFormat(DateError):
    """Raised if a date format string is invalid."""


class InvalidInput(DateError):
    """Raised if user input is invalid."""


def parse_query(query):
    """Return :class:`~datetime.date` or None"""
    m = QUERY_MATCH(query)
    if not m:
        return None

    sign = m.group(1) or '+'
    count = int(m.group(2))
    unit = m.group(3).lower()

    log.debug('sign=%s, count=%s, units=%s', sign, count, unit)

    if unit == 'w':
        count = count * 7

    elif unit == 'y':
        count = count * 365

    if sign == '+':
        return date.today() + timedelta(days=count)

    elif sign == '-':
        return date.today() - timedelta(days=count)

    raise ValueError('unknown sign: ' + sign)


def date_with_format(dt, fmt):
    """Return ``datetime.date`` formatted for output with date format."""
    fmt, lc = parse_date_format(fmt)
    set_locale(lc)
    result = dt.strftime(fmt)
    set_locale()
    return result


def get_default_locale():
    """Return system language"""
    output = run_command(['defaults', 'read', '-g', 'AppleLanguages'])
    output = output.strip('()\n ')

    langs = [s.strip('", ').replace('-', '_') for s in output.split('\n')]

    if not len(langs):
        raise ValueError('could not determine system locale')

    return langs[0]


def parse_date_format(dateformat):
    """Return ``(fmt, locale)``.

    ``locale`` defaults to system locale if not in ``dateformat``
    """
    lc = None

    m = LANG_SEARCH(dateformat)
    if m:
        lc = m.group(1)
        fmt = dateformat[:m.start(0)] + dateformat[m.end(0):]
    else:
        fmt = dateformat
    log.debug('locale=%s,  dateformat=%s', lc, fmt)
    return (fmt, lc)


def format_valid(fmt):
    """Return ``True`` if ``fmt`` is valid, else ``False``"""
    fmt, lc = parse_date_format(fmt)
    try:
        date.today().strftime(fmt)
    except ValueError:
        return False
    return True


def set_locale(lc=None):
    """Python libs don't work inside Alfred. Use ``defaults`` instead"""
    if not lc:
        lc = get_default_locale()

    log.debug('locale=%r', lc)

    try:
        locale.setlocale(locale.LC_ALL, (lc, 'UTF-8'))
    except locale.Error:
        locale.setlocale(locale.LC_ALL, (lc[:2], 'UTF-8'))


def get_default_formats():
    """Return default formats for locale."""
    lc, encoding = locale.getlocale()
    return DEFAULT_DATE_FORMATS.get(lc, FALLBACK_DATE_FORMATS)


def get_formats():
    """Return saved custom formats or defaults for locale."""
    wf = Workflow()

    if 'date_formats' not in wf.settings:
        wf.settings['date_formats'] = get_default_formats()

    return wf.settings.get('date_formats')
