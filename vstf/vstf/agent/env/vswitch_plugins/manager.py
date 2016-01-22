##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import stevedore


class VswitchPluginManager(object):
    def __init__(self):
        self.plugin = None
        self.mgr = stevedore.extension.ExtensionManager(namespace="vswitch.plugins", invoke_on_load=True)

    def clean(self):
        if self.plugin:
            self.plugin.clean()
            self.plugin = None
        for plugin in self.mgr.names():
            self.mgr[plugin].obj.clean()
        return True

    def get_vs_plugin(self, plugin):
        if plugin in self.mgr.names():
            ext = self.mgr[plugin]
            self.plugin = ext.obj
            return self.plugin
        else:
            raise Exception("unsupported vswitch plugin: %s" % plugin)

    def get_supported_plugins(self):
        return self.mgr.names()
