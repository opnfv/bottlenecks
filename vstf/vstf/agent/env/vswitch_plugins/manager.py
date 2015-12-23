"""
Created on 2015-9-15

@author: y00228926
"""
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
