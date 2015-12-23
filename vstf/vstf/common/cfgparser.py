"""
Created on 2015-8-5

@author: c00225995
"""
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
