'''
Created on 2015-9-24

@author: y00228926
'''
import unittest
import time
import subprocess

from vstf.agent.unittest.perf import model
from vstf.agent.perf import netperf
from vstf.agent.perf.utils import get_pid_by_name


class TestNetperf(model.Model):
    '''
    please make sure 'Tn' network on 'Target Host' is created.
    '''
    def setUp(self):
        super(TestNetperf, self).setUp()
        subprocess.call("killall netperf", shell = True)
        subprocess.call("killall netserver",shell = True)
        for ns, dev, ip_setting in zip(self.ns_list, self.device_list, self.ip_setting_list):
            netdev = {
                  "namespace":ns,
                  "iface":dev,
                  'ip_setting':ip_setting
            }
            self.mgr.config_dev(netdev)
        self.send_cfg = {
            "namespace": "send",
            "protocol": "udp_bw",
            "dst":[
                    {"ip": "192.168.1.2"}
                ],
            "size": 64,
            "threads": 1,
            "time": 10, 
        }
  
    def tearDown(self):
        super(TestNetperf, self).tearDown()
    
    def test_netperf_start_success(self):
        perf = netperf.Netperf()
        ret = perf.receive_start(namespace='receive')
        exp = (0, 'start netserver success')
        self.assertEqual(ret, exp, "receive_start failed %s" % str(ret))
        
        ret = perf.send_start(**self.send_cfg)
        exp = (0,"start netperf send success")
        self.assertEqual(ret, exp, "failed to start netperf")
        
        time.sleep(3)
        
        ret = perf.send_stop()
        exp = [(0, "process is stopped by killed")]
        self.assertEqual(ret, exp, "send_stop failed, ret = %s" % str(ret)) 
          
        ret = perf.receive_stop()
        exp = (0, "stop netserver success")
        self.assertEqual(ret, exp, "receive_stop failedf, ret = %s" % str(ret)) 
    
    def test_netperf_start_success_mutil_threads(self):
        perf = netperf.Netperf()
        ret = perf.receive_start(namespace='receive')
        exp = (0, 'start netserver success')
        self.assertEqual(ret, exp, "receive_start failed %s" % str(ret))
        
        self.send_cfg.update({"threads":3})
        exp = (0,"start netperf send success")
        ret = perf.send_start(**self.send_cfg)
        self.assertEqual(ret, exp, "failed to start netperf")
        
        time.sleep(3)
        
        rets = perf.send_stop()
        exp = [(0, 'process is stopped by killed'), (0, 'process is stopped by killed'), (0, 'process is stopped by killed')]
        self.assertEqual(rets, exp, "send_stop failed, rets = %s" % str(rets)) 
          
        rets = perf.receive_stop()
        self.assertEqual(rets, (0, "stop netserver success"), "receive_stop failedf, rets = %s" % str(rets))
    
    def test_clean(self):
        perf = netperf.Netperf()
        ret = perf.receive_start(namespace='receive')
        exp = (0, 'start netserver success')
        self.assertEqual(ret, exp, "receive_start failed %s" % str(ret))
        
        self.send_cfg.update({"threads":3})
        exp = (0,"start netperf send success")
        ret = perf.send_start(**self.send_cfg)
        self.assertEqual(ret, exp, "failed to start netperf")
        perf.clean()
        ret = get_pid_by_name('netperf')
        self.assertEqual(ret, [], "failed to clean netperf")
        ret = get_pid_by_name('netserver')
        self.assertEqual(ret, [], "failed to clean netserver")
            
if __name__ == "__main__":
    import logging
    logging.getLogger(__name__)
    logging.basicConfig(level = logging.DEBUG)
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()