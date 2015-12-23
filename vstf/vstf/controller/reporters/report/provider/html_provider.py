#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-25
# see license for license details
__version__ = ''' '''
import logging

LOG = logging.getLogger(__name__)
from vstf.controller.settings.html_settings import HtmlSettings
from vstf.controller.settings.data_settings import DataSettings


class HtmlProvider(object):
    def __init__(self, content, style):
        self._content = content
        self._style = style

    def get_style(self):
        return self._style["style"]

    def get_subject(self):
        return self._content["subject"]

    def get_ovs_title(self):
        return self._content["ovs"]["title"]

    def get_ovs_table(self):
        return map(lambda x: list(x), self._content["ovs"]["content"].items())

    def get_result_title(self):
        return self._content["result"]["title"]

    def get_result_table(self, ttype):
        result = []
        content = self._content["result"]["content"]
        if ttype in content:
            result.append(content[ttype]["columns"])
            result.extend(content[ttype]["data"])

            result = map(lambda x: list(x), zip(*result))
        return result


class StyleProvider(object):
    def __init__(self, style):
        self._style = style

    def get_style(self):
        return self._style["style"]


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/html-provder.log", clevel=logging.INFO)

    html_settings = HtmlSettings()
    LOG.info(html_settings.settings)
    data_settings = DataSettings()
    LOG.info(data_settings.settings)

    hprovider = HtmlProvider(data_settings.settings, html_settings.settings)
    sprovider = StyleProvider(html_settings.settings)
