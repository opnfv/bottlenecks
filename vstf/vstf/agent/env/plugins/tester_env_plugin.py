#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015/11/17
# see license for license details

import logging

from vstf.agent.env.plugins.model import EnvBuilderPlugin
from vstf.agent.env.driver_plugins.manager import DriverPluginManager

LOG = logging.getLogger(__name__)


class Plugin(EnvBuilderPlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.dr_mgr = DriverPluginManager()

    def clean(self):
        self.dr_mgr.clean()

    def install(self):
        pass

    def load_drivers(self):
        drivers = self.host_cfg['drivers']
        self.dr_mgr.load(drivers)

    def create_brs(self):
        pass

    def config_br_ports(self):
        pass

    def create_vms(self):
        pass

    def wait_vms(self):
        pass

    def check_vm_connectivity(self):
        pass
