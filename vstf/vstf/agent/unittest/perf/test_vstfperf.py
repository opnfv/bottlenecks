"""
Created on 2015-9-28

@author: y00228926
"""
import unittest

from vstf.agent.perf.vstfperf import Vstfperf
from vstf.agent.unittest.perf import model


class Test(model.Model):
    def setUp(self):
        super(Test, self).setUp()
        
        for ns, dev, ip_setting in zip(self.ns_list, self.device_list, self.ip_setting_list):
            net_dev = {
                  "namespace":ns,
                  "iface":dev,
                  'ip_setting':ip_setting
            }
            self.mgr.config_dev(net_dev)
            
        self.start = {
            "operation": "start",
            "action": "send",
            "tool": "netperf",
            "params":{
                "namespace": self.ns_list[0],
                "protocol": "tcp_lat",
                "dst":[
                        {"ip": self.ip_list[1]}
                    ],
                "size": 64,
                "threads": 1,
                "time": 1,  
            },
        }
        self.stop = {
            "operation": "stop",
            "action": "send",
            "tool": "netperf",
            "params":{
                "namespace": self.ns_list[1],
            },
        }
        
    def tearDown(self):
        super(Test, self).tearDown()

    def testNetperf(self):
        perf = Vstfperf()
        self.start['tool'] = 'netperf'
        self.stop['tool'] = 'netperf'
        self.start['action'] = 'receive'
        self.start['operation'] = 'start'
        self.start['params']['namespace'] = self.ns_list[1]
        self.start['params']['protocol'] = 'udp_bw'
        perf.run(**self.start)
        self.start['action'] = 'send'
        self.start['operation'] = 'start'
        self.start['params']['namespace'] = self.ns_list[0]
        perf.run(**self.start)
        self.stop['action'] = 'send'
        self.stop['operation'] = 'stop'
        self.stop['params']['namespace'] = self.ns_list[0]
        perf.run(**self.stop)
        self.stop['action'] = 'receive'
        self.stop['operation'] = 'stop'
        self.stop['params']['namespace'] = self.ns_list[1]
        perf.run(**self.stop)
        
    def testQperf(self):
        perf = Vstfperf()
        self.start['tool'] = 'qperf'
        self.stop['tool'] = 'qperf'
        self.start['action'] = 'receive'
        self.start['operation'] = 'start'
        self.start['params']['namespace'] = self.ns_list[1]
        perf.run(**self.start)
        self.start['action'] = 'send'
        self.start['operation'] = 'start'
        self.start['params']['namespace'] = self.ns_list[0]
        perf.run(**self.start)
        self.stop['action'] = 'send'
        self.stop['operation'] = 'stop'
        self.stop['params']['namespace'] = self.ns_list[0]
        perf.run(**self.stop)
        self.stop['action'] = 'receive'
        self.stop['operation'] = 'stop'
        self.stop['params']['namespace'] = self.ns_list[1]
        perf.run(**self.stop)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.DEBUG)
    unittest.main()