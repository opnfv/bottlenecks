#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
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
        self.fetch_os_file = os.path.join(
            self.code_dir,
            'infra_setup',
            'fetch_os_creds.sh')

        with open(config_dir) as file:
            config_info = yaml.load(file)
            common_config = config_info['common_config']
            self.RELENG_DIR = common_config["releng_dir"]
            self.OS_FETCH_SCRIPT = common_config["fetch_os_file"]
            self.logdir = common_config['log_dir']
            self.OPENSTACK_RC_FILE = common_config['rc_dir']
            self.config_dir_check(self.logdir)

    def config_read(self, testcase, story_name):
        testcase_parser = {}
        self.story_dir = os.path.join(
            self.test_dir,
            testcase,
            'testsuite_story',
            story_name)
        with open(self.story_dir) as file:
            story_parser = yaml.load(file)
        for case_name in story_parser['testcase']:
            testcase_dir = os.path.join(
                self.test_dir,
                testcase,
                'testcase_cfg',
                case_name)
            with open(testcase_dir) as f:
                testcase_parser[case_name] = yaml.load(f)

        return testcase_parser

    def config_dir_check(self, dirname):
        if dirname is None:
            dirname = '/tmp/'
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def config_parser(self, testcase_cfg, parameters):
        test_cfg = testcase_cfg['test_config']
        stack_cfg = testcase_cfg['stack_config']
        # TO-DO add cli parameters to stack_config.
        return test_cfg, stack_cfg
