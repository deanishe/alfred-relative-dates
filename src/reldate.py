#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-03-12
#

"""Alfred 3 Script Filter to display formatted dates."""

from __future__ import print_function, unicode_literals

from datetime import date
import locale
import os
import sys

from workflow import Workflow3, ICON_ERROR


UPDATE_SETTINGS = {
    'github_slug': 'deanishe/alfred-relative-dates'
}


log = None


def main(wf):
    """Run workflow."""
    import common

    common.set_locale()

    # Whether script filter is being run from a snippet trigger
    snippet = os.getenv('snippet') is not None

    lc, encoding = locale.getlocale()

    log.debug('args: %r', wf.args)
    log.debug('locale=%s,  encoding=%s, snippet=%r', lc, encoding, snippet)

    query = wf.args[0].strip()

    log.debug('query=%r', query)

    if not query and wf.update_available:
        wf.add_item(
            'An Update is Available',
            '↩ or ⇥ to install',
            valid=False,
            icon='update.png'
        )

    if not query or query in ('0', 'now', 'today'):
        dt = date.today()
    else:
        dt = common.parse_query(query)

    if not dt:  # Didn't understand query
        wf.add_item("Couldn't understand '{}'".format(query),
                    "Use 'datehelp' for help on formatting",
                    valid=False, icon=ICON_ERROR)
        wf.send_feedback()
        return 0
    log.debug('date : {0.year}-{0.month}-{0.day}'.format(dt))

    # get date formats
    for i, fmt in enumerate(common.get_formats()):
        value = unicode(common.date_with_format(dt, fmt), encoding)

        sub = 'Copy to clipboard'
        action = 'copy'
        if snippet:
            sub = 'Paste in active app'
            action = 'paste'

        it = wf.add_item(value,
                         sub,
                         arg=value,
                         valid=True,
                         uid='date-{:02d}'.format(i),
                         icon='icon.png')

        it.setvar('action', action)

        if not snippet:
            mod = it.add_modifier('cmd', 'Paste in active app')
            mod.setvar('action', 'paste')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
