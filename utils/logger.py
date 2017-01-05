#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
# Logging levels:
#  Level     Numeric value
#  CRITICAL  50
#  ERROR     40
#  WARNING   30
#  INFO      20
#  DEBUG     10
#  NOTSET    0

import logging
import os

# from bottlenecks_cfg import Bottlenecks_cfg as bn_cfg


class Logger:
    def __init__(self, logger_name):
        
        #if user set --debug as a cli parameter
        #we will set this variable “Debug” to output debug info.
        DEBUG = os.getenv('DEBUG')

        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = 0
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        log_formatter = ('%(asctime)s '
                         '%(name)s %(filename)s:%(lineno)d '
                         '%(levelname)s %(message)s')

        formatter = logging.Formatter(log_formatter)

        ch.setFormatter(formatter)
        if DEBUG is not None and DEBUG.lower() == "true":
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)

#        result_path = bn_cfg.['log_dir']
#        if not os.path.exists(result_path):
#            os.makedirs(result_path)
        hdlr = logging.FileHandler('/tmp/bottlenecks.log')
        hdlr.setFormatter(formatter)
        hdlr.setLevel(logging.DEBUG)
        self.logger.addHandler(hdlr)

    def getLogger(self):
        return self.logger