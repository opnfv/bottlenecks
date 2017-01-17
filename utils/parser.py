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

    bottlenecks_config = {}

    @classmethod
    def config_init(cls):
        cls.code_dir = os.path.dirname(os.path.abspath(__file__))
        cls.root_dir = os.path.dirname(cls.code_dir)
        cls.test_dir = os.path.join(cls.root_dir, 'testsuites')
        config_dir = os.path.join(
            cls.root_dir,
            'config',
            'config.yaml')

        with open(config_dir) as file:
            config_info = yaml.load(file)
            common_config = config_info['common_config']
            cls.bottlenecks_config["releng_dir"] = common_config["releng_dir"]
            cls.bottlenecks_config["fetch_os"] = common_config["fetch_os_file"]
            cls.bottlenecks_config["log_dir"] = common_config['log_dir']
            cls.bottlenecks_config["rc_dir"] = common_config['rc_dir']
            cls.config_dir_check(cls.bottlenecks_config["log_dir"])

    @classmethod
    def config_read(cls, testcase, story_name):
        story_dir = os.path.join(
            cls.test_dir,
            testcase,
            'testsuite_story',
            story_name)
        with open(story_dir) as file:
            story_parser = yaml.load(file)
        for case_name in story_parser['testcase']:
            testcase_dir = os.path.join(
                cls.test_dir,
                testcase,
                'testcase_cfg',
                case_name)
            with open(testcase_dir) as f:
                cls.bottlenecks_config[case_name] = yaml.load(f)

        return cls.bottlenecks_config

    @classmethod
    def config_dir_check(cls, dirname):
        if dirname is None:
            dirname = '/tmp/'
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    @staticmethod
    def config_parser(testcase_cfg, parameters):
        test_cfg = testcase_cfg['test_config']
        stack_cfg = testcase_cfg['stack_config']
        # TO-DO add cli parameters to stack_config.
        return test_cfg, stack_cfg
