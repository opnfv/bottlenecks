##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging

import stevedore

LOG = logging.getLogger(__name__)


class PluginManager(object):

    def __init__(self):
        self.instance = None
        self.saved = {}

    def build(self, cfg):
        scheme = cfg["scheme"]
        if scheme in self.saved:
            # reuse old instance
            self.instance = self.saved[scheme]
        else:
            mgr = stevedore.driver.DriverManager(namespace="env_build.plugins",
                                                 name=scheme,
                                                 invoke_on_load=False)
            self.instance = mgr.driver()
            self.saved[scheme] = self.instance

        self.instance.clean()
        return self.instance.build(cfg)

    def clean(self):
        if self.instance:
            self.instance.clean()
        self.instance = None


if __name__ == "__main__":
    import argparse
    from vstf.controller.env_build.env_build import IntentParser

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file to parse')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    parser = IntentParser(args.config)
    cfg_intent = parser.parse_cfg_file()
    for host_cfg in cfg_intent['env-build']:
        tn = PluginManager()
        tn.build(host_cfg)
