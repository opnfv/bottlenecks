#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09.25
# see license for license details
__version__ = ''' '''

import os
from vstf.common.pyhtml import *


class HtmlBase(object):
    def __init__(self, provider, ofile='text.html'):
        self._page = PyHtml('HtmlBase Text')
        self._ofile = ofile
        self._provider = provider
        self._chapter = 1

    def save(self):
        if self._ofile:
            os.system('rm -rf %s' % self._ofile)
            self._page.output(self._ofile)

    def as_string(self):
        return self._page.as_string()

    def add_table(self, data):
        self._page.add_table(data)

    def add_style(self):
        style = self._provider.get_style()
        self._page.add_style(style)

    def create(self, is_save=True):
        self.add_style()
        self.create_story()
        if is_save:
            self.save()
        return self.as_string()

    def create_story(self):
        raise NotImplementedError("abstract HtmlBase")
