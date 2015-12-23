"""
Created on 2015-9-23

@author: y00228926
"""
import unittest

from vstf.agent.unittest.perf import model
from vstf.agent.perf import netns


class TestNetnsManager(model.Model):
    def setUp(self):
        super(TestNetnsManager, self).setUp()
        self.ns = netns.Netns()
                
    def tearDown(self):
        super(TestNetnsManager, self).tearDown()

    def testNetns(self):
        device_list,ns_list,ip_setting_list,ip_list = self.device_list,self.ns_list,self.ip_setting_list,self.ip_list
        net = self.ns
        for ns in ns_list:
            self.assertTrue(net.create_namespace(ns),'create_namespace failed')
        for ns,dev,ip_setting in zip(ns_list,device_list,ip_setting_list):
            self.assertTrue(net.add_device(ns, dev),'add_device failed')
            self.assertTrue(net.activate_device(ns,dev),'activate_device failed')
            self.assertTrue(net.config_ip(ns,dev,ip_setting),'config_ip failed')
        for ns in ns_list:
            self.assertTrue(net.remove_namespace(ns),'remove_namespace failed')
    
    def testNetNsManager(self):
        mgr = self.mgr
        device_list,ns_list,ip_setting_list,ip_list = self.device_list,self.ns_list,self.ip_setting_list,self.ip_list
        for ns,dev,ip_setting in zip(ns_list,device_list,ip_setting_list):
            netdev = {
                      "namespace":ns,
                      "iface":dev,
                      'ip_setting':ip_setting
                }
            ret = mgr.config_dev(netdev)
            self.assertTrue(ret,"config_dev failed, netdev=%s" % netdev)
            
        for ns,dev,ip_setting in zip(ns_list,device_list,ip_setting_list):
            netdev = {
                      "namespace":ns,
                      "iface":dev,
                      'ip_setting':ip_setting
                }
            self.assertTrue(mgr.recover_dev(netdev),"recover_dev failed, netdev=%s" % netdev)
            
        for ns,dev,ip_setting in zip(ns_list,device_list,ip_setting_list):
            netdev = {
                      "namespace":ns,
                      "iface":dev,
                      'ip_setting':ip_setting
                }
            self.assertTrue(mgr.config_dev(netdev),"config_dev failed, netdev=%s" % netdev)       
        self.assertTrue(mgr.clean_all_namespace(),'remove_namespace failed')


if __name__ == "__main__":
    import logging
    LOG = logging.getLogger(__name__)
    logging.basicConfig(level = logging.DEBUG)
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()