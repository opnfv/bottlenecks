#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from setuptools import setup, find_packages


setup(
        name="bottlenecks",
        version="master",
        py_modules=['bottlenecks_cli'],
        packages=find_packages(),
        include_package_data=True,
        package_data={
                    'utils': [
                                    'utils/infra_setup/heat/*.py',
                                    'utils/infra_setup/runner/*.py'
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
