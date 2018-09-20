#!/usr/bin/env python
##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file realize the function of how to setup server of test-scheduler
to your environment. This use setuptools tool to setup'''

from setuptools import setup, find_packages


setup(
    name="test-scheduler-server",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'src': [
            'env/config/license',
            'env/context/*.yaml',
            'env/service/*.yaml',
            'conductor_processor/*.json'
        ],
        'test': [
            'test_case/*/*.yaml'
        ]
    }
)
