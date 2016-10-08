##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import logging

import vstf.common.candy_text as candy
from vstf.controller.reporters.report.provider.html_provider import HtmlProvider
from vstf.controller.settings.template_settings import TemplateSettings
from vstf.controller.settings.html_settings import HtmlSettings
from vstf.controller.reporters.report.html.html_base import HtmlBase, pyhtm

LOG = logging.getLogger(__name__)


class HtmlCreator(HtmlBase):

    def create_story(self):
        self.add_context()

    def add_context(self):
        context = self._provider.get_context
        self._raw_context(context)

    def _raw_context(self, context, ci=0, si=0, ui=0, level=-1):
        _story = []
        for key, value in sorted(context.items()):
            LOG.info(key)
            LOG.info(value)
            _sn, _node, _style = candy.text2tuple(key)
            if _node in candy.dom:
                if _node == candy.chapter:
                    ci = _style
                elif _node == candy.section:
                    si = _style
                else:
                    ui = _style
                self._raw_context(value, ci, si, ui, level + 1)

            else:
                LOG.info("node: %s  %s" % (_node, candy.title))
                if _node == candy.title:
                    assert value
                    if level in range(len(candy.dom)):
                        if level == 0:
                            value[0] = "Chapter %s %s" % (ci, value[0])
                            for title in value:
                                self._page << pyhtm.H2(title)
                        elif level == 1:
                            value[0] = "%s.%s %s" % (ci, si, value[0])
                            for title in value:
                                self._page << pyhtm.H3(title)
                        else:
                            value[0] = "%s.%s.%s %s" % (ci, si, ui, value[0])
                            for title in value:
                                self._page << pyhtm.H3(title)

                elif _node == candy.table:
                    self.add_table(value)
                elif _node == candy.paragraph:
                    for para in value:
                        para = pyhtm.space(2) + para
                        self._page << pyhtm.P(para)


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/html-creator.log",
        clevel=logging.INFO)

    out_file = "vstf_report.html"

    info = TemplateSettings()
    html_settings = HtmlSettings()
    provider = HtmlProvider(info.settings, html_settings.settings)
    reporter = HtmlCreator(provider)
    reporter.create(out_file)

if __name__ == '__main__':
    unit_test()
