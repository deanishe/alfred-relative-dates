#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-03-12
#

"""formats.py [options] <action> [<format>]

Usage:
    formats.py (-h | --help)
    formats.py show [<format>]
    formats.py edit <format>

Options:
    -h, --help  Show this help message.
"""

from __future__ import print_function, unicode_literals

import sys
import os
from datetime import date

from workflow import Workflow, ICON_INFO, ICON_WARNING, ICON_ERROR
from common import set_locale, get_all_formats


log = None


def format_valid(fmt):
    """Return ``True`` if ``fmt`` is valid, else ``False``"""
    try:
        s = date.today().strftime(fmt)
    except ValueError:
        return False
    return True


def main(wf):
    from docopt import docopt

    set_locale()

    args = docopt(__doc__, argv=wf.args)
    log.debug('args : {}'.format(args))
    fmt = args.get('<format>')

    custom_formats = wf.settings.get('custom_formats', [])

    if args.get('show'):
        if fmt:  # handle entered format
            if fmt in get_all_formats():
                wf.add_item("'{}' already exists".format(fmt),
                            'Try something else',
                            valid=False,
                            icon=ICON_WARNING)
            elif not format_valid(fmt):
                wf.add_item("'{}' is not a valid date format".format(fmt),
                            "Use 'dthelp' for formatting help",
                            valid=False,
                            icon=ICON_WARNING)
            else:
                value = unicode(date.today().strftime(fmt), 'utf-8')
                wf.add_item("Save '{}' to custom formats".format(fmt),
                            'e.g. {}'.format(value),
                            valid=True,
                            arg=fmt,
                            icon='icon.png')

        elif not custom_formats:  # warn of no formats
            wf.add_item('You have no custom formats',
                        'Type one in and hit ↩ to save it',
                        valid=False,
                        icon=ICON_INFO)

        else:  # list custom formats
            wf.add_item('Hit ↩ on a saved format to delete it',
                        valid=False, icon=ICON_INFO)
            for f in custom_formats:
                value = unicode(date.today().strftime(f), 'utf-8')
                wf.add_item(f,
                            'e.g. {}'.format(value),
                            valid=True,
                            arg=f,
                            icon='icon.png')

        wf.send_feedback()
        return 0

    elif args.get('edit'):  # delete if format exists, else add
        if fmt in custom_formats:
            custom_formats.remove(fmt)
            print("Deleted '{}'".format(fmt))
        else:
            custom_formats.append(fmt)
            custom_formats.sort()
            print("Saved '{}'".format(fmt))

        wf.settings['custom_formats'] = custom_formats


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
