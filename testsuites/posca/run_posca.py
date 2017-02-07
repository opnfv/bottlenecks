#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of how to run posca.
In this file, The first thing is to read testcase config
for example: you could run this by use
posca_run('testcase', "Which testcase you will run")
posca_run('teststory', "Which story you will run")
and if you run "python run_posca", this will run testcase,
posca_factor_system_bandwidth by default.'''

import importlib
import utils.parser as conf_parser
import utils.logger as log
INTERPRETER = "/usr/bin/python"

LOG = log.Logger(__name__).getLogger()
# ------------------------------------------------------
# run posca testcase
# ------------------------------------------------------


def posca_testcase_run(testcase_script, test_config):

    module_string = "testsuites.posca.testcase_script.%s" % (testcase_script)
    module = importlib.import_module(module_string)
    module.run(test_config)


def posca_run(test_level, test_name):
    if test_level == "testcase":
        config = conf_parser.Parser.testcase_read("posca", test_name)
    elif test_level == "teststory":
        config = conf_parser.Parser.story_read("posca", test_name)
    for testcase in config:
        LOG.info("Begin to run %s testcase in POSCA testsuite", testcase)
        posca_testcase_run(testcase, config[testcase])
        LOG.info("End of %s testcase in POSCA testsuite", testcase)


def main():
    test_level = "testcase"
    test_name = "posca_factor_system_bandwidth"
    posca_run(test_level, test_name)


if __name__ == '__main__':
    main()
