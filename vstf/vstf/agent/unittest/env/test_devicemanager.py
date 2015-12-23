"""
Created on 2015-9-25

@author: y00228926
"""
import unittest

from vstf.agent.unittest.env import model
from vstf.agent.env.basic.device_manager import DeviceManager


class Test(model.Test):
    def setUp(self):
        super(Test, self).setUp()
        self.dm = DeviceManager()
        self.device_list = self.dm.list_nic_devices()
        self.device_detail = self.device_list[0]

    def tearDown(self):
        super(Test, self).tearDown()

    def test_get_device_detail(self):
        detail1 = self.dm.get_device_detail(self.device_detail['bdf'])
        detail2 = self.dm.get_device_detail(self.device_detail['mac'])
        detail3 = self.dm.get_device_detail(self.device_detail['device'])
        self.assertTrue(detail1 == detail2 == detail3 == self.device_detail)

    def test_list_nic_devices(self):
        import json
        print json.dumps(self.device_list, indent=4)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    unittest.main()
