"""
Created on 2015-9-23

@author: y00228926
"""
import unittest
import time

from vstf.agent.perf.utils import get_pid_by_name
from vstf.agent.unittest.perf import model
from vstf.agent.perf import vnstat


class TestVnstat(model.LocalModel):
    def setUp(self):
        super(TestVnstat, self).setUp()
        self.vnstat = vnstat.VnStat()
        self.namespace = self.ns_list[0]
        self.device = self.device_list[0]
        self.ip_setting = self.ip_setting_list[0]
        netdev = {
            "namespace": self.namespace,
            "iface": self.device,
            'ip_setting': self.ip_setting
        }
        self.mgr.config_dev(netdev)

    def tearDown(self):
        super(TestVnstat, self).tearDown()

    def test_run_vnstat(self):
        logging.basicConfig(level=logging.DEBUG)
        pid = self.vnstat.run_vnstat(self.device, self.namespace)
        time.sleep(12)
        raw = self.vnstat.kill_vnstat(pid, self.namespace)
        print raw['raw_data']
        data = self.vnstat.process(raw['raw_data'])
        self.assertTrue(type(data) is dict)
        for key in ('rxmB/s', 'txmB', 'rxpck', 'txpck', \
                    'rxpck_min/s', 'txmB_max/s', 'txpck_max/s', \
                    'txmB/s', 'rxmB', 'rxmB_max/s', 'rxpck/s', 'rxmB_min/s', \
                    'time', 'rxpck_max/s', 'txpck_min/s', 'txpck/s', 'txmB_min/s'):
            self.assertTrue(key in data)

    def test_clean(self):
        self.vnstat.run_vnstat(self.device, self.namespace)
        self.vnstat.clean()
        self.assertTrue(get_pid_by_name('vnstat') == [])


if __name__ == "__main__":
    import logging

    LOG = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
