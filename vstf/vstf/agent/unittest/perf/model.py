"""
Created on 2015-9-25

@author: y00228926
"""
import unittest

from vstf.agent.unittest import configuration
from vstf.agent.perf import netns


class LocalModel(unittest.TestCase):
    def _ping(self):
        device_list, ns_list, ip_setting_list, ip_list = self.device_list, self.ns_list, self.ip_setting_list, self.ip_list
        for ns, dev, ip_setting in zip(ns_list, device_list, ip_setting_list):
            netdev = {
                "namespace": ns,
                "iface": dev,
                'ip_setting': ip_setting
            }
            self.mgr.config_dev(netdev)
        ip_list_copy = ip_list[:]
        ip_list_copy.reverse()
        for ns, ip in zip(ns_list, ip_list_copy):
            self.assertTrue(sself.mgr.ping(ns, ip), True)
        self.mgr.clean_all_namespace()

    def setUp(self):
        # make sure you have set up Tn loop on the "Target Host"
        self.mgr = netns.NetnsManager()
        self.mgr.clean_all_namespace()
        self.device_list = configuration.eth_for_test
        self.mac_list = configuration.mac_of_eth
        self.ns_list = ['send', 'receive']
        self.ip_setting_list = ['192.168.1.1/24', '192.168.1.2/24']
        self.ip_list = ['192.168.1.1', '192.168.1.2']

    def tearDown(self):
        self.mgr.clean_all_namespace()


class Model(LocalModel):
    def setUp(self):
        # make sure you have set up Tn loop on the "Target Host"
        super(Model, self).setUp()
        self._ping()
