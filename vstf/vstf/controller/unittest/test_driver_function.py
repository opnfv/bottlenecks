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

from vstf.controller.functiontest.driver.drivertest import config_setup
from vstf.controller.unittest import model


class TestDriverFunction(model.Test):   
    def setUp(self):
        logging.info("start driver function test unit test.")
        
    def test_config_setup(self):
        config ,_ = config_setup()
        for key in ("test_scene","bond_flag","switch_module"):
            self.assertTrue(key in config.keys(), "config_setup function failure.")

    def teardown(self):
        logging.info("stop driver function test unit test.")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)
    unittest.main()