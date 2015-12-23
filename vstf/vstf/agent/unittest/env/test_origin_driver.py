"""
Created on 2015-10-9

@author: y00228926
"""
import unittest

from vstf.common.utils import check_output
from vstf.agent.unittest.env import model
from vstf.agent.env.driver_plugins import origin_driver


class Test(model.Test):
    
    def setUp(self):
        super(Test, self).setUp()
        self.driver_mgr = origin_driver.OriginDriverPlugin()

    def tearDown(self):
        super(Test, self).tearDown()

    def _driver_exists(self, drivers=[]):
        all_drivers = check_output("lsmod | awk '{print $1}'",shell = True).split()
        for mod in drivers:
            if mod not in all_drivers:
                return False
        return True
                  
    def test_load(self):
        self.driver_mgr.clean()
        self.assertFalse(self._driver_exists(self.driver_mgr.get_supported_drivers()))
        
        self.driver_mgr.load(['ixgbe','vhost_net'])
        self.assertTrue(self._driver_exists(['ixgbe','vhost_net']))
        
        self.driver_mgr.clean()
        self.assertFalse(self._driver_exists(self.driver_mgr.get_supported_drivers()))


if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)
    LOG = logging.getLogger(__name__)
    unittest.main()