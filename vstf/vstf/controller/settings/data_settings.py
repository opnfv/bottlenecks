#!/usr/bin/env python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-09-25
# see license for license details

import logging

import vstf.controller.settings.settings as sets

LOG = logging.getLogger(__name__)


class DataSettings(sets.Settings):
    def __init__(self, path="/etc/vstf/reporter/",
                 filename="reporters.html.data-settings",
                 mode=sets.SETS_SINGLE):
        super(DataSettings, self).__init__(path, filename, mode)

    def _register_func(self):
        super(DataSettings, self)._register_func()
        items = {"ovs", "result"}
        fkeys = {"title", "content"}
        for item in items:
            item = item.encode()
            for key in fkeys:
                key = key.encode()
                func_name = "set_%s_%s" % (item, key)
                setattr(self, func_name, self._setting_file(func_name, self._mset[item], self._fset[item], key))
                func_name = "mset_%s_%s" % (item, key)
                setattr(self, func_name, self._setting_memory(func_name, self._mset[item], key))