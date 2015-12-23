"""
Created on 2015-9-24

@author: y00228926
"""
import unittest
import os

from vstf.controller.env_build.cfg_intent_parse import IntentParser
from vstf.agent.env import builder


class Test(unittest.TestCase):
    def setUp(self):
        self.mgr = builder.PluginManager()
        self.dir = os.path.dirname(__file__)

    def tearDown(self):
        self.mgr.clean()

    def __build(self, filepath, drivers=None):
        parser = IntentParser(filepath)
        cfg_intent = parser.parse_cfg_file()
        host_cfg = cfg_intent['env-build'][0]
        print filepath
        print host_cfg
        host_cfg["src-install"] = {}
        if drivers:
            host_cfg['drivers'] = drivers
        return self.mgr.build(host_cfg)

    def test_build_tn_using_origin_driver(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Tn.json'), drivers=['ixgbe'])
        self.assertTrue(ret, "test_build_tn_using_origin_driver failed, ret = %s" % ret)

    def test_build_tn1v_using_origin_driver(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Tn1v.json'), drivers=['ixgbe', 'vhost_net'])
        self.assertTrue(ret, "test_build_tn1v_using_origin_driver failed, ret = %s" % ret)

    def test_build_ti_using_origin_driver(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Ti.json'), drivers=['ixgbe', 'vhost_net'])
        self.assertTrue(ret, "test_build_ti_using_origin_driver failed, ret = %s" % ret)

    def test_build_tu_using_origin_driver(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Tu.json'), drivers=['vhost_net'])
        self.assertTrue(ret, "test_build_ti_using_origin_driver failed, ret = %s" % ret)

    @unittest.skip('can be tested by tn1v')
    def test_build_tn(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Tn.json'))
        self.assertTrue(ret, "test_build_tn failed, ret = %s" % ret)

    @unittest.skip('can be tested by tn1v')
    def test_build_tn1v(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Tn1v.json'))
        self.assertTrue(ret, "test_build_tn failed,ret = %s" % ret)

    @unittest.skip('can be tested by tn1v')
    def test_build_ti(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Ti.json'))
        self.assertTrue(ret, "test_build_tn failed, ret = %s" % ret)

    @unittest.skip('can be tested by tn1v')
    def test_build_tu(self):
        ret = self.__build(os.path.join(self.dir, 'configuration/Tu.json'))
        self.assertTrue(ret, "test_build_tn failed, ret = %s" % ret)


if __name__ == "__main__":
    import logging

    LOG = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
