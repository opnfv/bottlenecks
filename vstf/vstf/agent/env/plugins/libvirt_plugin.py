"""
Created on 2015-7-8

@author: y00228926
"""
import logging

from vstf.common.utils import ping, my_sleep
from vstf.agent.env.plugins.model import EnvBuilderPlugin
from vstf.agent.env.basic.source_manager import SourceCodeManager
from vstf.agent.env.basic.vm_manager import VMControlOperation
from vstf.agent.env.vswitch_plugins.manager import VswitchPluginManager
from vstf.agent.env.driver_plugins.manager import DriverPluginManager

LOG = logging.getLogger(__name__)


class Plugin(EnvBuilderPlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.vm_mgr = VMControlOperation()
        self.vs_mgr = VswitchPluginManager()
        self.dr_mgr = DriverPluginManager()

    def clean(self):
        self.vm_mgr.clean_all_vms()
        self.vs_mgr.clean()
        self.dr_mgr.clean()

    def load_drivers(self):
        drivers = self.host_cfg['drivers']
        self.dr_mgr.load(drivers)

    def create_brs(self):
        for br_cfg in self.host_cfg['bridges']:
            plugin = self.vs_mgr.get_vs_plugin(br_cfg['type'])
            plugin.create_br(br_cfg)

    def config_br_ports(self):
        for vm_cfg in self.host_cfg['vms']:
            for tap_cfg in vm_cfg['taps']:
                plugin = self.vs_mgr.get_vs_plugin(tap_cfg['br_type'])
                plugin.set_tap_vid(tap_cfg)
        for br_cfg in self.host_cfg['bridges']:
            plugin = self.vs_mgr.get_vs_plugin(br_cfg['type'])
            plugin.set_fastlink(br_cfg)

    def create_vms(self):
        for vm_cfg in self.host_cfg['vms']:
            self.vm_mgr.create_vm(vm_cfg)

    def wait_vms(self):
        for vm_cfg in self.host_cfg['vms']:
            self.vm_mgr.wait_vm(vm_cfg['vm_name'])
            self.vm_mgr.init_config_vm(vm_cfg['vm_name'])

    def check_vm_connectivity(self):
        for vm_cfg in self.host_cfg['vms']:
            vm_ip = vm_cfg['init_config']['ctrl_ip_setting'].split('/')[0]
            for _ in range(3):
                ret = ping(vm_ip)
                if ret:
                    break
                my_sleep(3)
            else:
                raise Exception("ping ip:%s failed." % vm_ip)
