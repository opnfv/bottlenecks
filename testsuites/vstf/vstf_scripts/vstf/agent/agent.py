##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# !/usr/bin/env python
# coding=utf-8

import logging
import argparse
import signal

from oslo.config import cfg

from vstf.rpc_frame_work import rpc_consumer
from vstf.common.log import setup_logging
from vstf.common import daemon
from vstf.common.cfgparser import CfgParser

LOG = logging.getLogger(__name__)

server_opts = [
    cfg.StrOpt('user', default='guest', help="the rabbit's user, default guest"),
    cfg.StrOpt('passwd', default='guest', help="the rabbit's passwd, default guest"),
    cfg.StrOpt('host', default='localhost', help="tell the process wich interface to listen"),
    cfg.StrOpt('port', default=5672, help=""),
    cfg.StrOpt('id', default='agent', help="")

]

stc_opts = [
    cfg.StrOpt('package', default='', help="the STC python path")
]


class Client(daemon.Daemon):
    """This is a consumer of vstf-agent which will create two channel to the
    rabbitmq-server, one for direct call, one for fan call.

    agent start with a config file which record rabbitmq's ip, port and user passwd
    also each agent has its own id.

    """

    def __init__(self, agent, config_file):
        """Record the config file, init the daemon.

        :param str config_file: the config of a VSTF agent.

        """
        super(Client, self).__init__('/tmp/esp_rpc_client.pid')
        self.config_file = config_file
        self.agent = agent
        self.config = None
        self.proxy = None
        self.run_flag = True

    def init_config(self):
        """Use olso.config to analyse the config file

        """
        parser = CfgParser(self.config_file)
        parser.register_my_opts(server_opts, "rabbit")
        parser.register_my_opts(stc_opts, "spirent")
        self.config = parser.parse()

    def loop_thread(self):
        LOG.info("Try to create direct proxy...")
        self.proxy = rpc_consumer.VstfConsumer(self.agent,
                                               self.config.rabbit.user,
                                               self.config.rabbit.passwd,
                                               self.config.rabbit.host,
                                               self.config.rabbit.port,
                                               self.config.rabbit.id)
        self.proxy.run()

    def run(self):
        """Run the rabbitmq consumers as a daemon.

        """
        signal.signal(signal.SIGTERM, self.process_exit)
        self.loop_thread()
        LOG.info("agent start ok!")

    def process_exit(self, signum, frame):
        """This function try to stop the agent after running agent stop.
        When we call vstf-agent stop which will send a signal SIGTERM to agent
        When the agent catch the SIGTERM signal will call this function.

        """
        LOG.info("daemon catch the signalterm, start to stop the process.")
        self.run_flag = False
        if self.proxy:
            self.proxy.stop()

    def start_agent(self):
        self.init_config()
        self.start()

    def stop_agent(self):
        """Notice that: this function just kill the agent by pid file, it has
        none vars of the agent.

        """
        LOG.info("call daemon stop.")
        # kill the main thread
        self.stop()


def main():
    setup_logging(level=logging.INFO, log_file="/var/log/vstf/vstf-agent.log")
    parser = argparse.ArgumentParser(description='agent option')
    parser.add_argument('action', choices=('start', 'stop', "restart"),
                        default="start", help="start or stop agent")
    parser.add_argument('--agent_type', action='store',
                        default="soft",
                        choices=["soft", "spirent"],
                        help="the agent type, as now, just soft and spirent")
    parser.add_argument(
        '--config_file',
        action='store',
        default="/etc/vstf/amqp/amqp.ini",
        help="some env_build params recorded in the config file")

    args = parser.parse_args()

    client = Client(args.agent_type, args.config_file)
    if "start" == args.action:
        client.start_agent()
    elif "stop" == args.action:
        client.stop_agent()
    elif "restart" == args.action:
        client.stop_agent()
        client.start_agent()
    else:
        raise Exception("only support actions: start/stop/restart")


if __name__ == '__main__':
    main()
