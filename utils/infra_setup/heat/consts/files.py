##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# ------------------------------------------------------
# Configuration File
# ------------------------------------------------------
GENERAL = 'General'


def get_sections():
    return [
        GENERAL,
        # Add here new configurations...
    ]


def get_sections_api():
    return [
        GENERAL,
        # Add here new configurations...
    ]

# ------------------------------------------------------
# General section parameters
# ------------------------------------------------------
ITERATIONS = 'iterations'
TEMPLATE_DIR = 'template_dir'
TEMPLATE_NAME = 'template_base_name'
BENCHMARKS = 'benchmarks'
DEBUG = 'debug'
