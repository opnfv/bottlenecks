##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

__version__ = ''' '''

import os
import vstf.common.pyhtml as pyhtm


class HtmlBase(object):
    def __init__(self, provider):
        self._page = pyhtm.PyHtml('Html Text')
        self._provider = provider

    def save(self, ofile):
        if ofile:
            os.system('rm -rf %s' % ofile)
            self._page.output(ofile)

    def as_string(self):
        return self._page.as_string()

    def add_table(self, data):
        if data and zip(*data):
            self._page.add_table(data)

    def add_style(self):
        style = self._provider.get_style
        self._page.add_style(style)

    def create(self, ofile='text.html'):
        self.add_style()
        self.create_story()
        self.save(ofile)
        return self.as_string()

    def create_story(self):
        raise NotImplementedError("abstract HtmlBase")
