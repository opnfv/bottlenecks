#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os


class Testcase(object):
    """Test command group.

       Set of commnads to execute and list testcases
    """

    def __init__(self):
        self.test_case_path = '/home/opnfv/bottlenecks/testsuites/'
        self.test_case_list = []

    def run(self, testname, noclean=False):
    	os.system('bash /home/opnfv/bottlenecks/run_tests.sh '+testname)
