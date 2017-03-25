#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of how to setup bottlenecks
to your environment. This use setuptools tool to setup'''

from setuptools import setup, find_packages


setup(
    name="bottlenecks",
    version="0.1",
    py_modules=['cli/bottlenecks_cli'],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'utils': [
            '*.py'
        ],
        'config': [
            '*.yaml'
        ],
        'testsuites': [
            'posca/testcase_cfg/*',
            'posca/testcase_script/*',
            'posca/testsuite_story/*',
            'posca/testcase_dashboard/*'
        ],
    },
    url="https://www.opnfv.org",
    install_requires=["click"],
    entry_points={
        'console_scripts': [
            'bottlenecks=cli.bottlenecks_cli:main'
        ],
    },
)
