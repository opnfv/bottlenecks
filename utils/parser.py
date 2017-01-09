#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from logger import Logger
import os
import yaml


class Parser():
    def __init__(self):
        self.code_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.code_dir)
        self.test_dir = os.path.join(self.root_dir, 'testsuites')
        config_dir = os.path.join(
            self.root_dir,
            'config',
            'config.yaml')
        with open(config_dir) as file:
            log_info = yaml.load(file)
            self.logdir = log_info['common_config']
        self.LOG = Logger(__name__).getLogger()

    def config_read(self, testcase, story_name):
        self.LOG.info("begin to parser config file!")
        testcase_parser = {}
        self.story_dir = os.path.join(
            self.test_dir,
            testcase,
            'testsuite_story',
            story_name)
        with open(self.story_dir) as file:
            self.LOG.info('testsuite:' + testcase + 'story:' + story_name)
            story_parser = yaml.load(file)
        for case_name in story_parser['testcase']:
            testcase_dir = os.path.join(
                self.test_dir,
                testcase,
                'testcase_cfg',
                case_name)
            with open(testcase_dir) as f:
                self.LOG.info('story: %s, testcase: %s' % (story_name, case_name))
                testcase_parser[case_name] = yaml.load(f)

        return testcase_parser

    def config_parser(self, testcase_cfg, parameters):
        test_cfg = testcase_cfg['test_config']
        stack_cfg = testcase_cfg['stack_config']
        # TO-DO add cli parameters to stack_config.
        return test_cfg, stack_cfg