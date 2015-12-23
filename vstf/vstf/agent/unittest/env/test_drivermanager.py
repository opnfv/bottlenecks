"""
Created on 2015-10-9

@author: y00228926
"""
import unittest

from vstf.common.utils import check_output
from vstf.agent.unittest.env import model
from vstf.agent.env.driver_plugins import manager


class Test(model.Test):
    def setUp(self):
        super(Test, self).setUp()
        self.driver_mgr = manager.DriverPluginManager()

    def tearDown(self):
        super(Test, self).tearDown()

    def _driver_exists(self, drivers=[]):
        all_drivers = check_output("lsmod | awk '{print $1}'", shell=True).split()
        for mod in drivers:
            if mod not in all_drivers:
                return False
        return True

    def test_load(self):
        self.driver_mgr.clean()
        for _, drivers in self.driver_mgr.get_all_supported_drivers().items():
            self.assertFalse(self._driver_exists(drivers))


        self.driver_mgr.load(['ixgbe', 'vhost_net'])
        self.assertTrue(self._driver_exists(['ixgbe', 'vhost_net']))

        self.driver_mgr.clean()
        self.assertFalse(self._driver_exists(['ixgbe', 'vhost_net']))

    def test_load_unsuported_pair(self):
        with self.assertRaises(Exception):
            self.driver_mgr.load(['ixgbe', 'tap_vhost'])


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    unittest.main()
