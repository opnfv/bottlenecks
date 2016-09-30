##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging

LOG = logging.getLogger(__name__)
from vstf.controller.settings.html_settings import HtmlSettings
from vstf.controller.settings.template_settings import TemplateSettings


class HtmlProvider(object):

    def __init__(self, info, style):
        self._info = info
        self._style = style

    @property
    def get_style(self):
        assert "style" in self._style
        return self._style["style"]

    @property
    def get_context(self):
        assert "context" in self._info
        return self._info["context"]


def main():
    from vstf.common.log import setup_logging
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/html-provder.log",
        clevel=logging.INFO)

    html_settings = HtmlSettings()
    LOG.info(html_settings.settings)
    info = TemplateSettings()
    provider = HtmlProvider(info.settings, html_settings.settings)
    LOG.info(provider.get_style)
    LOG.info(provider.get_context)

if __name__ == '__main__':
    main()
