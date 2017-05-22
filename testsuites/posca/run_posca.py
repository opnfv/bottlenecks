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
import sys
import os

from oslo_serialization import jsonutils
import requests
import datetime

import utils.parser as conf_parser
import utils.logger as log
INTERPRETER = "/usr/bin/python"

LOG = log.Logger(__name__).getLogger()
# ------------------------------------------------------
# run testcase in posca
# ------------------------------------------------------


def posca_testcase_run(testcase_script, test_config):

    module_string = "testsuites.posca.testcase_script.%s" % (testcase_script)
    module = importlib.import_module(module_string)
    module.run(test_config)


def report(testcase, start_date, stop_date, criteria, details_doc):
    headers = {'Content-type': 'application/json'}
    results = {
        "project_name": "bottlenecks",
        "description": ("test results for %s", testcase),
        "pod_name": os.environ.get('NODE_NAME', 'unknown'),
        "installer": os.environ.get('INSTALLER_TYPE', 'unknown'),
        "version": os.environ.get('YARDSTICK_VERSION', 'unknown'),
        "build_tag": os.environ.get('BUILD_TAG'),
        "stop_date": stop_date,
        "start_date": start_date,
        "criteria": criteria,
        "scenario": os.environ.get('DEPLOY_SCENARIO', 'unknown')
    }
    results['details'] = {"test_results": details_doc}

    target = "http://testresults.opnfv.org/test/api/v1/results"
    timeout = 5

    try:
        LOG.debug('Test result : %s', jsonutils.dump_as_bytes(results))
        res = requests.post(target=target,
                            data=jsonutils.dump_as_bytes(results),
                            headers=headers,
                            timeout=timeout)
        LOG.debug('Test result posting finished with status code'
                  ' %d.' % res.status_code)
    except Exception as err:
        LOG.exception('Failed to record result data: %s', err)


def posca_run(test_level, test_name, report="False"):
    if test_level == "testcase":
        config = conf_parser.Parser.testcase_read("posca", test_name)
    elif test_level == "teststory":
        config = conf_parser.Parser.story_read("posca", test_name)
    for testcase in config:
        LOG.info("Begin to run %s testcase in POSCA testsuite", testcase)
        config[testcase]['out_file'] =\
            conf_parser.Parser.testcase_out_dir(testcase)
        start_date = datetime.datetime.now()
        posca_testcase_run(testcase, config[testcase])
        stop_date = datetime.datetime.now()
        LOG.info("End of %s testcase in POSCA testsuite", testcase)

        if report is "True":
            details_doc = []
            with open(config[testcase]['out_file']) as details_result:
                lines = details_result.readlines()
                if len(lines):
                    criteria = "PASS"
                    for l in lines:
                        details_doc.append(l.replace('\n', ''))
                else:
                    criteria = "FAIL"
            report(testcase, start_date, stop_date, criteria, details_doc)


def main():
    test_level = sys.argv[1]
    test_name = sys.argv[2]
    report = sys.argv[3]
    posca_run(test_level, test_name, report)


if __name__ == '__main__':
    main()
