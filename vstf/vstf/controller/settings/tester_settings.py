#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015/11/17
# see license for license details

import logging

import vstf.controller.settings.settings as sets

LOG = logging.getLogger(__name__)


class TesterSettings(sets.Settings):
    def __init__(self, path="/etc/vstf/env/",
                 filename="tester.json",
                 mode=sets.SETS_SINGLE):
        super(TesterSettings, self).__init__(path, filename, mode)
