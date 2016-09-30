##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import unittest

from vstf.controller.unittest import model
from vstf.controller.env_build.cfg_intent_parse import IntentParser


class Test(model.Test):

    def setUp(self):
        super(Test, self).setUp()
        self.dir = os.path.dirname(__file__)

    def tearDown(self):
        super(Test, self).tearDown()

    def test_parse_cfg_file(self):
        for m in ['Ti', 'Tu', 'Tn', 'Tnv']:
            filepath = os.path.join(self.dir, 'configuration/env/%s.json' % m)
            parser = IntentParser(filepath)
            parser.parse_cfg_file()


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    unittest.main()
