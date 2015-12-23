"""
Created on 2015-9-24

@author: y00228926
"""
import unittest
import time

from vstf.agent.unittest.perf import model
from vstf.agent.perf import pktgen


class TestPktgen(model.Model):
    def setUp(self):
        super(TestPktgen, self).setUp()

    def tearDown(self):
        super(TestPktgen, self).tearDown()

    def test_single_thread(self):
        perf = pktgen.Pktgen()
        print perf.receive_start()
        send = {
            "src": [
                {"iface": self.device_list[0], "mac": self.mac_list[0]}
            ],
            "dst": [
                {"mac": self.mac_list[1]}
            ],
            "size": 64,
            "threads": 1,
            'ratep': 0
        }
        ret = perf.send_start(**send)
        self.assertEqual((0, 'start pktgen send success'), ret, "send_start failed, ret=%s" % str(ret))
        time.sleep(5)
        ret = perf.send_stop()
        self.assertEqual([(0, '')], ret, "send_start failed, ret=%s" % ret)
        ret = perf.receive_stop()
        self.assertEqual((0, 'pktgen neednt receive stop'), ret, "send_stop failed, ret=%s" % str(ret))

    def test_single_thread_bidirectional(self):
        perf = pktgen.Pktgen()
        print perf.receive_start()
        send = {
            "src": [
                {"iface": self.device_list[0], "mac": self.mac_list[0]},
                {"iface": self.device_list[1], "mac": self.mac_list[1]}
            ],
            "dst": [
                {"mac": self.mac_list[1]},
                {"mac": self.mac_list[0]}
            ],
            "size": 64,
            "threads": 1,
            'ratep': 0
        }
        ret = perf.send_start(**send)
        self.assertEqual((0, 'start pktgen send success'), ret, "send_start failed, ret=%s" % str(ret))
        time.sleep(5)
        ret = perf.send_stop()
        self.assertEqual([(0, '')], ret, "send_start failed, ret=%s" % ret)
        ret = perf.receive_stop()
        self.assertEqual((0, 'pktgen neednt receive stop'), ret, "send_stop failed, ret=%s" % str(ret))

    def test_clean(self):
        perf = pktgen.Pktgen()
        print perf.receive_start()
        send = {
            "src": [
                {"iface": self.device_list[0], "mac": self.mac_list[0]}
            ],
            "dst": [
                {"mac": self.mac_list[1]}
            ],
            "size": 64,
            "threads": 1,
            'ratep': 0
        }
        ret = perf.send_start(**send)
        self.assertEqual((0, 'start pktgen send success'), ret, "send_start failed, ret=%s" % str(ret))
        perf.clean()


if __name__ == "__main__":
    import logging

    logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
