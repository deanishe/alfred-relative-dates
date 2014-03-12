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
from datetime import date, timedelta
import re
import locale

from workflow import Workflow, ICON_ERROR
from common import set_locale, get_all_formats


log = None
QUERY_MATCH = re.compile(r"""([+-]{0,1})(\d+)([d|w|y])""",
                         re.IGNORECASE).match



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
    return date.today() + timedelta(days=count)


def main(wf):
    log.debug('-' * 40)
    set_locale()
    lc, encoding = locale.getlocale()
    log.debug('args : {}'.format(wf.args))
    log.debug('locale : {}  encoding : {}'.format(lc, encoding))
    query = wf.args[0]
    log.debug('query : {}'.format(query))
    dt = parse_query(query)
    if not dt:  # Didn't understand query
        wf.add_item("Couldn't understand '{}'".format(query),
                    "Use 'dthelp' for help on formatting",
                    valid=False, icon=ICON_ERROR)
        wf.send_feedback()
        return 0
    log.debug('date : {0.year}-{0.month}-{0.day}'.format(dt))
    # get date formats
    for fmt in get_all_formats():
        value = unicode(dt.strftime(fmt), encoding)
        wf.add_item(value,
                    'Copy to clipboard',
                    arg=value,
                    valid=True,
                    icon='icon.png')
    wf.send_feedback()
    log.debug('finished.')


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
