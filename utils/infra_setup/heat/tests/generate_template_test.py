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
import mock

import sys
sys.path.append("..")
import template
import common

def reset_common():
    common.LOG = None
    common.CONF_FILE = None
    common.DEPLOYMENT_UNIT = None
    common.ITERATIONS = None
    common.BASE_DIR = None
    common.TEMPLATE_DIR = None
    common.TEMPLATE_NAME = None
    common.TEMPLATE_EXTENSION = None

class TestGeneratesTemplate(unittest.TestCase):
    def setUp(self):
        self.deployment_configuration = {
            'flavor': ['medium']
        }
        self.template_name = 'rubbos_1-1-1_template.tmp'
        # common.init()

    def tearDown(self):
        reset_common()

    @mock.patch('common.LOG')
    @mock.patch('common.get_template_dir')
    def test_generates_template_for_success(self, mock_template_dir,
                                            mock_log):
        tmp_generated_templates_dir = '/data/generated_templates/'
        generated_templates_dir = "{}{}".format(os.getcwd(), tmp_generated_templates_dir)
        mock_template_dir.return_value = generated_templates_dir
        tmp_test_templates = '/data/test_templates/'
        test_templates = "{}{}".format(os.getcwd(), tmp_test_templates)
        template.generates_templates(self.template_name,
                                     self.deployment_configuration)
        for dirname, dirnames, filenames in os.walk(test_templates):
            for filename in filenames:
                with open(test_templates + filename) as test:
                    with open(generated_templates_dir + filename) as generated:
                        self.assertListEqual(test.readlines(),
                                             generated.readlines())

        t_name = '/data/generated_templates/rubbos_1-1-1_template.tmp'
        self.template_name = "{}{}".format(os.getcwd(), t_name)
        template.generates_templates(self.template_name,
                                     self.deployment_configuration)
        for dirname, dirnames, filenames in os.walk(test_templates):
            for filename in filenames:
                with open(test_templates + filename) as test:
                    with open(generated_templates_dir + filename) as generated:
                        self.assertListEqual(test.readlines(),
                                             generated.readlines())

    @mock.patch('common.get_template_dir')
    def test_get_all_heat_templates_for_success(self, template_dir):
        tmp_generated_templates = '/data/generated_templates/'
        generated_templates = "{}{}".format(os.getcwd(), tmp_generated_templates)
        template_dir.return_value = generated_templates
        extension = '.yaml'
        expected = ['test_template_1.yaml']
        result = template.get_all_heat_templates(generated_templates,
                                                 extension)
        self.assertListEqual(expected, result)
