"""
Created on 2015-9-24

@author: y00228926
"""
import unittest
from vstf.common import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ns_cmd(self):
        cmd = "ls"
        ns = "xx"
        exp_cmd = "ip netns exec xx ls"
        ret = utils.ns_cmd(ns, cmd)
        self.assertEqual(ret, exp_cmd, "ns_cmd failed to add ns header prefix:%s != %s" % (ret, exp_cmd))


if __name__ == "__main__":
    import logging

    logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
