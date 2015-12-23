'''
Created on 2015-9-24

@author: y00228926
'''
import unittest
import subprocess
import time

from vstf.agent.unittest.perf import model
from vstf.agent.perf import qperf
from vstf.agent.perf.utils import get_pid_by_name


class testQperf(model.Model):
    def setUp(self):
        super(testQperf, self).setUp()
        subprocess.call("killall qperf", shell = True)
        for ns, dev, ip_setting in zip(self.ns_list, self.device_list, self.ip_setting_list):
            netdev = {
                  "namespace":ns,
                  "iface":dev,
                  'ip_setting':ip_setting
            }
            self.mgr.config_dev(netdev)
        self.send_cfg = {
            "namespace": self.ns_list[0],
            "time":1,
            "protocol": "udp_lat",
            "dst":[
                    {"ip": self.ip_list[1]}
                ],
            "size": 64,
        }
        
    def tearDown(self):
        super(testQperf, self).tearDown()

    def test_qperf_quick(self):
        perf = qperf.Qperf()
        ret = perf.receive_start(namespace=self.ns_list[1])
        exp = (0, "start qperf receive success")
        self.assertEqual(ret, exp, "receive_start failed %s" % str(ret))
        
        ret = perf.send_start(**self.send_cfg)
        exp = (0,"start qperf send success")
        self.assertEqual(ret, exp, "send_start failed")
        
        time.sleep(3)
        
        ret = perf.send_stop()
        for r in ret:
            self.assertEqual(r[0], 0, "send_stop failed, ret = %s" % str(ret))
            for key in ('MaximumLatency', 'AverageLatency', 'MinimumLatency'):
                self.assertIn(key, r[1], "send_stop failed, ret = %s" % str(ret))
          
        ret = perf.receive_stop()
        exp = (0, "stop qperf receive success")
        self.assertEqual(ret, exp, "receive_stop failed, ret = %s" % str(ret)) 
    
    def test_qperf_quick_3s(self):
        perf = qperf.Qperf()
        self.send_cfg.update({"time":3})
        ret = perf.receive_start(namespace='receive')
        exp = (0, 'start qperf receive success')
        self.assertEqual(ret, exp, "receive_start failed %s" % str(ret))
        
        self.send_cfg.update({"threads":3})
        exp = (0,"start qperf send success")
        ret = perf.send_start(**self.send_cfg)
        self.assertEqual(ret, exp, "send_start failed %s" % str(ret))
        
        ret = perf.send_stop()
        for r in ret:
            self.assertEqual(r[0], 0, "send_stop failed, ret = %s" % str(ret))
            for key in ('MaximumLatency', 'AverageLatency', 'MinimumLatency'):
                self.assertIn(key, r[1], "send_stop failed, ret = %s" % str(ret))
          
        ret = perf.receive_stop()
        self.assertEqual(ret, (0, 'stop qperf receive success'), "receive_stop failedf, ret = %s" % str(ret))
    
    def test_clean(self):
        perf = qperf.Qperf()
        self.send_cfg.update({"time":10})
        ret = perf.receive_start(namespace=self.ns_list[1])
        exp = (0, "start qperf receive success")
        self.assertEqual(ret, exp, "receive_start failed %s" % str(ret))
        
        ret = perf.send_start(**self.send_cfg)
        exp = (0,"start qperf send success")
        self.assertEqual(ret, exp, "send_start failed")  
        
        perf.clean()
        ret = get_pid_by_name('qperf')
        self.assertEqual(ret, [], "clean qperf failed")      


if __name__ == "__main__":
    import logging
    logging.getLogger(__name__)
    logging.basicConfig(level = logging.DEBUG)
    unittest.main()