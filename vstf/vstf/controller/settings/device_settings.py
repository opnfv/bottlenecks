#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015/11/19
# see license for license details

import logging

import vstf.controller.settings.settings as sets

LOG = logging.getLogger(__name__)


class DeviceSettings(sets.Settings):
    def __init__(self, path="/etc/vstf/perf/",
                 filename="sw_perf.device-settings",
                 mode=sets.SETS_SINGLE):
        super(DeviceSettings, self).__init__(path, filename, mode)
