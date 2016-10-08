##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import stevedore


class DriverPluginManager(object):

    def __init__(self):
        self.plugins = {}
        self.mgr = stevedore.extension.ExtensionManager(
            namespace="drivers.plugins", invoke_on_load=True)

    def load(self, drivers):
        plugin = self.determine_driver_type(drivers)
        ext = self.mgr[plugin]
        ext.obj.load(drivers)
        return True

    def clean(self):
        self.mgr.map(self._clean)
        return True

    def _clean(self, ext, *args, **kwargs):
        ext.obj.clean()

    def get_all_supported_drivers(self):
        if not self.plugins:
            for ext_name in self.mgr.names():
                ext = self.mgr[ext_name]
                self.plugins[ext_name] = ext.obj.get_supported_drivers()
        return self.plugins

    def determine_driver_type(self, drivers):
        s = set(drivers)
        for plugin, supported in self.get_all_supported_drivers().items():
            if not (s - set(supported)):
                return plugin
        else:
            raise Exception('unspported drivers: %s' % drivers)
