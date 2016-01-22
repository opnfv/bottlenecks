##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging

from vstf.controller.fabricant import Fabricant
from vstf.rpc_frame_work.rpc_producer import Server
from vstf.controller.env_build.cfg_intent_parse import IntentParser

LOG = logging.getLogger(__name__)


class EnvBuildApi(object):
    def __init__(self, conn, config_file):
        LOG.info("welcome to EnvBuilder")
        self.conn = conn
        intent_parser = IntentParser(config_file)
        self.cfg_intent = intent_parser.parse_cfg_file()

    def build(self):
        LOG.info("start build")
        for host_cfg in self.cfg_intent['env-build']:
            rpc = Fabricant(host_cfg['ip'], self.conn)
            rpc.build_env(timeout=1800, cfg_intent=host_cfg)
        return True

    def clean(self):
        for host_cfg in self.cfg_intent['env-build']:
            rpc = Fabricant(host_cfg['ip'], self.conn)
            rpc.clean_env(timeout=120)
        return True

    def get_hosts(self):
        result = []
        for host_cfg in self.cfg_intent['env-build']:
            host = {
                'name': host_cfg['ip'],
                'nic': "82599ES 10-Gigabit"
            }
            result.append(host)
        return result


class TransmitterBuild(object):
    def __init__(self, conn, config_file):
        LOG.info("welcome to TransmitterBuild")
        self.conn = conn
        self._cfg_intent = config_file["transmitter-build"]

    def build(self):
        LOG.info("start build")
        for cfg in self.cfg_intent:
            rpc = Fabricant(cfg['ip'], self.conn)
            cfg.setdefault("scheme", 'transmitter')
            rpc.build_env(timeout=1800, cfg_intent=cfg)
        return True

    def clean(self):
        for cfg in self.cfg_intent:
            rpc = Fabricant(cfg['ip'], self.conn)
            rpc.clean_env(timeout=10)
        return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--rpc_server', help='rabbitmq server for deliver messages.')
    parser.add_argument('--config', help='config file to parse')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    conn = Server(args.rpc_server)
    tn = EnvBuildApi(conn, args.config)
    tn.build()
