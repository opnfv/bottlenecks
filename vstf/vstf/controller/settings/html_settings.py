#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-25
# see license for license details
__version__ = ''' '''

import logging

import vstf.controller.settings.settings as sets

LOG = logging.getLogger(__name__)


class HtmlSettings(sets.Settings):
    def __init__(self, path="/etc/vstf/", filename="reporters.html-settings", mode=sets.SETS_DEFAULT):
        super(HtmlSettings, self).__init__(path, filename, mode)


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/html-settings.log", clevel=logging.DEBUG)
    html_settings = HtmlSettings()
    style = {
        'table': {
            'font-family': '"Trebuchet MS", Arial, Helvetica, sans-serif',
            'border-collapse': 'collapse',
            'border': '1px solid green',
            'padding': '8px',
            'text-align': 'center'
        },
        'td':
            {
                'border': '1px solid green',
                'padding': '8px',
                'word-wrap': 'break-all'
            },
        'th':
            {
                'background-color': '#EAF2D3',
                'border': '1px solid green',
                'padding': '8px'
            }
    }

    html_settings.set_style(style)
    LOG.info(html_settings.settings)


if __name__ == '__main__':
    unit_test()
