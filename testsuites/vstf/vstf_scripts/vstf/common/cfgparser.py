##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
from oslo.config import cfg


class CfgParser(object):

    def __init__(self, config_file):
        super(CfgParser, self).__init__()
        if os.path.isfile(config_file) is False:
            raise Exception('The config file not found <%s>' % config_file)
        self.config_file = config_file
        self.CONF = cfg.ConfigOpts()

    def register_my_opts(self, opts, name=None):
        if name:
            self.CONF.register_opts(opts, name)
        else:
            self.CONF.register_opts(opts)

    def parse(self):
        #  self.register_my_opts(opts, name=name)
        self.CONF(args=[], default_config_files=[self.config_file])
        return self.CONF
