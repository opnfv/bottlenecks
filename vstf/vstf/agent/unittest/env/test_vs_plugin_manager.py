"""
Created on 2015-9-24

@author: y00228926
"""
import unittest

from vstf.agent.unittest.env import model
from vstf.agent.env.vswitch_plugins import manager
from vstf.common.utils import check_call


class TestVsPlugins(model.Test):
    def setUp(self):
        super(TestVsPlugins, self).setUp()
        self.cfg = {
            "type": "ovs",
            "name": "ovs1",
            "uplinks": [
                {
                    "bdf": self.bdf_of_eth[0],
                    "vlan_mode": "trunk",
                    "vlan_id": "100,200,300,400"
                },
                {
                    "bdf": self.bdf_of_eth[1],
                    "vlan_mode": "trunk",
                    "vlan_id": "100,200,300,400"
                }
            ],
            "vtep": {}
        }
        self.mgr = manager.VswitchPluginManager()

    def tearDown(self):
        super(TestVsPlugins, self).tearDown()

    def _check_br_exists(self, name):
        try:
            check_call('ifconfig %s' % name, shell=True)
        except Exception, e:
            return False
        return True

    def test_create_bridge(self):
        self.cfg['name'] = 'br1'
        self.br = self.mgr.get_vs_plugin('bridge')
        self.br.clean()
        self.br.init()
        self.br.create_br(self.cfg)
        self.assertTrue(self._check_br_exists('br1'))
        self.br.clean()
        self.assertFalse(self._check_br_exists('br1'))

    def test_clean(self):
        self.mgr.clean()

    def test_get_supported_plugins(self):
        ret = self.mgr.get_supported_plugins()
        self.assertEqual(set(ret), {'bridge',  'ovs'})


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    unittest.main()
