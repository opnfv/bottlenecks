##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################



__version__ = ''' '''
import logging

LOG = logging.getLogger(__name__)
from vstf.controller.settings.template_settings import TemplateSettings


class PdfProvider(object):
    def __init__(self, info):
        self._info = info

    @property
    def get_theme(self):
        assert "theme" in self._info
        return self._info["theme"]

    @property
    def ifcontents(self):
        assert "contents" in self._info
        assert "enable" in self._info["contents"]
        return self._info["contents"]["enable"]

    @property
    def get_context(self):
        assert "context" in self._info
        return self._info["context"]


def main():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/pdf-provider.log", clevel=logging.INFO)

    info = TemplateSettings()
    provider = PdfProvider(info.settings)
    LOG.info(provider.get_theme)
    LOG.info(provider.ifcontents)
    LOG.info(provider.get_context)

if __name__ == '__main__':
    main()