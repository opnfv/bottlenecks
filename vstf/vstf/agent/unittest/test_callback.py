"""
Created on 2015-9-28

@author: y00228926
"""
import unittest

from vstf.agent.unittest.perf import model
from vstf.agent import softagent


class TestCallback(model.Model):
    def setUp(self):
        super(TestCallback, self).setUp()
        self.agent = softagent.softAgent()
        for ns, dev, ip_setting in zip(self.ns_list, self.device_list, self.ip_setting_list):
            netdev = {
                "namespace": ns,
                "iface": dev,
                'ip_setting': ip_setting
            }
            self.mgr.config_dev(netdev)

        self.start = {
            "operation": "start",
            "action": "send",
            "tool": "netperf",
            "params": {
                "namespace": self.ns_list[0],
                "protocol": "tcp_lat",
                "dst": [
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
            "params": {
                "namespace": self.ns_list[1],
            },
        }

    def tearDown(self):
        super(TestCallback, self).tearDown()

    def test_clean(self):
        agent = self.agent
        agent.perf_clean()
        self.start['tool'] = 'netperf'
        self.stop['tool'] = 'netperf'
        self.start['action'] = 'receive'
        self.start['operation'] = 'start'
        self.start['params']['namespace'] = self.ns_list[1]
        self.start['params']['protocol'] = 'udp_bw'
        agent.perf_run(**self.start)
        self.start['action'] = 'send'
        self.start['operation'] = 'start'
        self.start['params']['namespace'] = self.ns_list[0]
        agent.perf_run(**self.start)
        agent.perf_clean()


if __name__ == "__main__":
    import logging

    logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
