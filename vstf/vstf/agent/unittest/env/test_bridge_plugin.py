"""
Created on 2015-10-12

@author: y00228926
"""
import unittest

from vstf.common.utils import check_call
from vstf.agent.unittest.env import model
from vstf.agent.env.vswitch_plugins import bridge_plugin
from vstf.agent.env.driver_plugins import manager


class Test(model.Test):
    def setUp(self):
        super(Test, self).setUp()
        self.plugin = bridge_plugin.BridgePlugin()
        self.dr_mgr = manager.DriverPluginManager()
        self.br_cfg = {
            "name": "br1",
            "uplinks": [
                {
                    "bdf": self.bdf_of_eth[0],
                },
                {
                    "bdf": self.bdf_of_eth[1],
                }
            ]
        }
        self.dr_mgr.clean()
        self.dr_mgr.load(['ixgbe'])

    def tearDown(self):
        super(Test, self).tearDown()

    def _check_br_exists(self, name):
        try:
            check_call('ifconfig %s' % name, shell=True)
        except Exception, e:
            return False
        return True

    def test_create_br(self):
        self.plugin.clean()
        self.plugin.create_br(self.br_cfg)
        self.assertTrue(self._check_br_exists(self.br_cfg['name']))
        self.plugin.clean()
        self.assertFalse(self._check_br_exists(self.br_cfg['name']))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    unittest.main()
