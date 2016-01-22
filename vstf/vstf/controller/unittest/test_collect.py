##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import unittest
import json

from vstf.controller.env_build import env_collect
from vstf.controller.unittest import model


class TestCollect(model.Test):
    
    def setUp(self):
        super(TestCollect, self).setUp()
        self.obj = env_collect.EnvCollectApi(self.conn)
        
    def test_collect_host_info(self):
        ret_str = json.dumps(self.obj.collect_host_info(self.tester_host), indent = 4)
        for key in ("CPU INFO","MEMORY INFO","HW_INFO","OS INFO"):
            self.assertTrue(key in ret_str, "collect_host_info failed, ret_str = %s" % ret_str)
            
    def test_list_nic_devices(self):
        ret_str = json.dumps(self.obj.list_nic_devices(self.tester_host), indent = 4)
        for key in ("device","mac","bdf","desc"):
            self.assertTrue(key in ret_str, "list_nic_devices failed, ret_str = %s" % ret_str)
        print ret_str
    
    def test_get_device_detail(self):
        identity = "01:00.0"
        ret = self.obj.get_device_detail(self.tester_host, "01:00.0")
        for key in ("device","mac","bdf","desc"):
            self.assertTrue(key in ret)
        self.assertTrue(ret['bdf'] == identity)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)
    unittest.main()