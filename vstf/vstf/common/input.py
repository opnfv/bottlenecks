##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

__author__ = 'wly'
__version__ = '0.1'

import os


def raw_choice(title):
    ret = {'Y': True, 'N': False}
    while True:
        os.system("clear")
        in_str = "\n%s:(y|n)  " % title
        uin = raw_input(in_str).title()
        if uin in ['Y', 'N']:
            break
    return ret[uin]
