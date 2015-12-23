#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-24
# see license for license details
__version__ = ''' '''

import logging

LOG = logging.getLogger(__name__)
import vstf.common.constants as cst
from vstf.controller.reporters.report.html.html_base import *


class HtmlCreator(HtmlBase):
    def add_subject(self):
        title = self._provider.get_subject()
        self._page << H1(title)

    def add_ovs(self):
        title = "%s %s" % (self._chapter, self._provider.get_ovs_title())
        self._page << H2(title)
        data = self._provider.get_ovs_table()
        self.add_table(data)
        self._chapter += 1

    def add_result(self):
        title = "%s %s" % (self._chapter, self._provider.get_result_title())
        self._page << H2(title)

        section = 1
        for ttype in cst.TTYPES:
            data = self._provider.get_result_table(ttype)
            if data:
                title = "%s.%s %s" % (self._chapter, section, ttype.title())
                self._page << H3(title)
                self.add_table(data)
                section += 1
        self._chapter += 1

    def create_story(self):
        self.add_subject()
        self.add_ovs()
        self.add_result()


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/html-test.log", clevel=logging.INFO)

    from vstf.controller.settings.html_settings import HtmlSettings
    from vstf.controller.settings.data_settings import DataSettings

    html_settings = HtmlSettings()
    LOG.info(html_settings.settings)
    data_settings = DataSettings()
    LOG.info(data_settings.settings)

    from vstf.controller.reporters.report.provider.html_provider import HtmlProvider
    provider = HtmlProvider(data_settings.settings, html_settings.settings)
    html = HtmlCreator(provider)

    result = html.create()
    print result


if __name__ == '__main__':
    unit_test()
