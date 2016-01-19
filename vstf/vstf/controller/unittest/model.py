##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import unittest

from vstf.rpc_frame_work import rpc_producer
from vstf.controller.unittest import configuration


class Test(unittest.TestCase):

    def setUp(self):
        self.controller = configuration.rabbit_mq_server
        self.tester_host = configuration.tester_host
        self.target_host = configuration.target_host
        self.source_repo = configuration.source_repo
        self.conn = rpc_producer.Server(self.controller)

    def tearDown(self):
        self.conn.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()