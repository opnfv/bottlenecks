##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import unittest

from vstf.common import ssh
from vstf.controller.unittest import model


class Test(model.Test):

    def setUp(self):
        super(Test, self).setUp()
        self.host = self.source_repo["ip"]
        self.user = self.source_repo["user"]
        self.passwd = self.source_repo["passwd"]

    def tearDown(self):
        super(Test, self).tearDown()

    def test_run_cmd(self):
        ssh.run_cmd(self.host, self.user, self.passwd, 'ls')


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
