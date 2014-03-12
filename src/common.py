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

import sys
import os
import subprocess
import locale
from datetime import date, timedelta
import re
from workflow import Workflow


LOCALE_MATCH = re.compile(r"""([a-z]{2}_[A-Z]{2}).*""").match


FALLBACK_DATE_FORMATS = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%a, %d %b %Y',
        '%a, %d %B %Y',
]

DEFAULT_DATE_FORMATS = {
    'en_GB': [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%a, %d %b. %Y',
        '%a, %d %B %Y',
        '%d %b. %Y',
        '%d %B %Y',
    ],
    'en_US': [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%a, %b. %d %Y',
        '%a, %B %d %Y',
        '%b. %d %Y',
        '%B %d %Y',
    ],
    'de_DE': [
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%a, %d. %b. %Y',
        '%a, %d. %B %Y',
        '%d. %b. %Y',
        '%d. %B %Y',
    ],
}


def set_locale():
    """Python libs don't work inside Alfred. Use ``defaults`` instead"""
    if not os.getenv('LANG'):
        output = subprocess.check_output(['defaults', 'read', '-g',
                                          'AppleLocale']).strip()
        m = LOCALE_MATCH(output)
        if not m:
            log.error('No locale found')
            return None
        lc = m.group(1)
        os.environ['LANG'] = '{}.UTF-8'.format(lc)
    locale.setlocale(locale.LC_ALL, '')


def get_default_formats():
    lc, encoding = locale.getlocale()
    return DEFAULT_DATE_FORMATS.get(lc, FALLBACK_DATE_FORMATS)


def get_all_formats():
    """Return combination of saved custom formats and defaults for locale"""
    custom_formats = Workflow().settings.get('custom_formats', [])
    return custom_formats + get_default_formats()
