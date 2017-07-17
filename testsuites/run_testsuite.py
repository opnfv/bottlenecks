#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of how to run testsuite.
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
import json
import time
import requests
import datetime

import utils.parser as conf_parser
import utils.logger as log
import utils.infra_setup.runner.docker_env as docker_env
INTERPRETER = "/usr/bin/python"

LOG = log.Logger(__name__).getLogger()
# ------------------------------------------------------
# run testcase in posca
# ------------------------------------------------------


def posca_testcase_run(testsuite, testcase_script, test_config):

    module_string = "testsuites.%s.testcase_script.%s" % (testsuite,
                                                          testcase_script)
    module = importlib.import_module(module_string)
    module.run(test_config)


def report(testcase, start_date, stop_date, criteria, details_doc):
    headers = {'Content-type': 'application/json'}
    results = {
        "project_name": "bottlenecks",
        "case_name": testcase,
        "description": ("test results for " + testcase),
        "pod_name": os.environ.get('NODE_NAME', 'unknown'),
        "installer": os.environ.get('INSTALLER_TYPE', 'unknown'),
        "version": os.environ.get('BRANCH', 'unknown'),
        "build_tag": os.environ.get('BUILD_TAG', 'unknown'),
        "stop_date": str(stop_date),
        "start_date": str(start_date),
        "criteria": criteria,
        "scenario": os.environ.get('DEPLOY_SCENARIO', 'unknown')
    }
    results['details'] = {"test_results": details_doc}

    target = "http://testresults.opnfv.org/test/api/v1/results"
    timeout = 5

    try:
        LOG.debug('Test result : %s', jsonutils.dump_as_bytes(results))
        res = requests.post(target,
                            data=jsonutils.dump_as_bytes(results),
                            headers=headers,
                            timeout=timeout)
        LOG.debug('Test result posting finished with status code'
                  ' %d.' % res.status_code)
    except Exception as err:
        LOG.exception('Failed to record result data: %s', err)


def docker_env_prepare(config):
    LOG.info("Begin to prepare docker environment")
    if 'contexts' in config.keys() and config["contexts"] is not None:
        context_config = config["contexts"]
        if 'yardstick' in context_config.keys() and \
           context_config["yardstick"] is not None:
            docker_env.env_yardstick(context_config['yardstick'])
            conf_parser.Parser.convert_docker_env(config, "yardstick")
        if 'dashboard' in context_config.keys() and \
           context_config["dashboard"] is not None:
            docker_env.env_elk(context_config['dashboard'])
            conf_parser.Parser.convert_docker_env(config, "dashboard")
            LOG.debug('Waiting for ELK init')
            time.sleep(15)
    LOG.info("Docker environment have prepared")
    return


def testsuite_run(test_level, test_name, REPORT="False"):
    tester_parser = test_name.split("_")
    if test_level == "testcase":
        config = conf_parser.Parser.testcase_read(tester_parser[0], test_name)
    elif test_level == "teststory":
        config = conf_parser.Parser.story_read(tester_parser[0], test_name)
    for testcase in config:
        LOG.info("Begin to run %s testcase in POSCA testsuite", testcase)
        config[testcase]['out_file'] =\
            conf_parser.Parser.testcase_out_dir(testcase)
        start_date = datetime.datetime.now()
        docker_env_prepare(config[testcase])
        posca_testcase_run(tester_parser[0], testcase, config[testcase])
        stop_date = datetime.datetime.now()
        LOG.info("End of %s testcase in POSCA testsuite", testcase)
        criteria = "FAIL"
        if REPORT == "True":
            details_doc = []
            if os.path.exists(config[testcase]['out_file']):
                with open(config[testcase]['out_file']) as details_result:
                    details_doc =[json.loads(data) for data in details_result.readlines()] # noqa
                    if len(details_doc):
                        criteria = "PASS"
            report(testcase, start_date, stop_date, criteria, details_doc)


def main():
    test_level = sys.argv[1]
    test_name = sys.argv[2]
    REPORT = sys.argv[3]
    testsuite_run(test_level, test_name, REPORT)


if __name__ == '__main__':
    main()
