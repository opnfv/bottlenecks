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
import sys
import subprocess

INTERPRETER = "/usr/bin/python"
#------------------------------------------------------
# run posca testcase
# ------------------------------------------------------
def posca_run(arg):
    print "========== run posca ==========="
    if(arg == "factor_system_bandwidth"):
        print "========== run posca_system_bandwidth ==========="
        cmd = '/home/opnfv/bottlenecks/testsuites/posca/testcase_script/posca_factor_system_bandwidth.py'
        pargs = [INTERPRETER,cmd]
        sub_result = subprocess.Popen(pargs)
        sub_result.wait()

def posca_env_check():
    print "========== posca env check ==========="

def main():
    para_testname = sys.argv[0]
    para_test_arg = sys.argv[1]
    posca_env_check()
    posca_run(para_test_arg)
    sys.exit(0)

if __name__=='__main__':
    main()
