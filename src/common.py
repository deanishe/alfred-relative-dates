#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-03-12
#

"""
"""

from __future__ import print_function, unicode_literals

import subprocess
import locale
from datetime import date, timedelta
import re
from workflow import Workflow


log = None


LOCALE_MATCH = re.compile(r"""([a-z]{2}_[A-Z]{2}).*""").match
LANG_SEARCH = re.compile(r"""LANG=([a-z]{2}(?:_[A-Z]{2})?)""",
                         re.IGNORECASE).search
QUERY_MATCH = re.compile(r"""([+-]{0,1})(\d+)([d|w|y])""",
                         re.IGNORECASE).match


FALLBACK_DATE_FORMATS = [
    '%x',
    '%Y-%m-%d',
    '%d %b %Y',
    '%d %B %Y',
]

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
    pass


class InvalidFormat(DateError):
    pass


class InvalidInput(DateError):
    pass


def parse_query(query):
    """Return :class:`~datetime.date` or None"""
    m = QUERY_MATCH(query)
    if not m:
        return None
    sign = m.group(1) or '+'
    count = int(m.group(2))
    unit = m.group(3).lower()
    log.debug('sign : {} count : {} units : {}'.format(sign, count, unit))
    if unit == 'w':
        count = count * 7
    elif unit == 'y':
        count = count * 365
    if sign == '+':
        return date.today() + timedelta(days=count)
    elif sign == '-':
        return date.today() - timedelta(days=count)
    raise ValueError('Unknown sign : {}'.format(sign))


def date_with_format(dt, fmt):
    """Return :class:`datetime.date` formatted for output with date
    format ``fmt``

    """

    fmt, lc = parse_date_format(fmt)
    set_locale(lc)
    result = dt.strftime(fmt)
    set_locale()
    return result


def get_default_locale():
    """Return system language"""
    output = subprocess.check_output(['defaults', 'read', '-g',
                                      'AppleLanguages'])
    output = output.strip('()\n ')
    langs = [s.strip('", ').replace('-', '_') for s in output.split('\n')]
    if not len(langs):
        raise ValueError('Could not determine system locale')
    return langs[0]


# def get_default_locale():
#     """Return system locale or raise :class:`ValueError`"""

#     if os.getenv('LANG'):
#         m = LOCALE_MATCH(os.getenv('LANG'))
#         if not m:
#             raise ValueError('Could not determine system locale')
#         return m.group(1)

#     output = subprocess.check_output(['defaults', 'read', '-g',
#                                       'AppleLocale']).strip()
#     m = LOCALE_MATCH(output)
#     if not m:
#         raise ValueError('Could not determine system locale')
#     return m.group(1)


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
    log.debug('locale : {}  dateformat: {}'.format(lc, fmt))
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

    log.debug('locale : {!r}'.format(lc))

    try:
        locale.setlocale(locale.LC_ALL, (lc, 'UTF-8'))
    except locale.Error:
        locale.setlocale(locale.LC_ALL, (lc[:2], 'UTF-8'))


def get_default_formats():
    lc, encoding = locale.getlocale()
    return DEFAULT_DATE_FORMATS.get(lc, FALLBACK_DATE_FORMATS)


def get_formats():
    """Return combination of saved custom formats and defaults for locale"""

    wf = Workflow()

    if not 'date_formats' in wf.settings:
        wf.settings['date_formats'] = get_default_formats()

    return wf.settings.get('date_formats')
