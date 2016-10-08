##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import uuid
import time
import os
import sys
import logging
import signal
import json

from vstf.common import unix, message, cliutil, excepts
from vstf.common.vstfcli import VstfParser
from vstf.common.log import setup_logging
from vstf.common import daemon
from vstf.controller.fabricant import Fabricant
from vstf.agent.env.basic.commandline import CommandLine
from vstf.controller.env_build.env_build import EnvBuildApi as Builder
from vstf.controller.env_build.env_collect import EnvCollectApi
from vstf.controller.database.dbinterface import DbManage
import vstf.controller.sw_perf.performance as pf
from vstf.controller.settings.tester_settings import TesterSettings
from vstf.controller.settings.device_settings import DeviceSettings
from vstf.controller.settings.flows_settings import FlowsSettings
from vstf.controller.settings.mail_settings import MailSettings
from vstf.controller.settings.tool_settings import ToolSettings
from vstf.controller.settings.perf_settings import PerfSettings
from vstf.controller.sw_perf.perf_provider import PerfProvider
from vstf.controller.sw_perf.flow_producer import FlowsProducer
from vstf.controller.settings.forwarding_settings import ForwardingSettings
import vstf.controller.reporters.reporter as rp
import vstf.rpc_frame_work.rpc_producer as rpc
import vstf.common.constants as cst
import vstf.common.check as chk

LOG = logging.getLogger(__name__)
cmd = CommandLine()


class OpsChains(object):

    def __init__(self, monitor, port):
        """The ops chains will setup the proxy to rabbitmq
        and setup a thread to watch the queues of rabbitmq

        """
        LOG.info("VSTF Manager start to listen to %s", monitor)
        if not os.path.exists(cst.VSTFCPATH):
            os.mkdir(cst.VSTFCPATH)

        self.chanl = rpc.Server(host=monitor, port=port)
        self.dbconn = DbManage()
        self.collection = EnvCollectApi(self.chanl)

    def list_devs(self, **kwargs):
        target = kwargs.get('host')
        if not target:
            respond = "the target is empty, not support now."
        else:
            respond = self.chanl.call(
                self.chanl.make_msg("list_nic_devices"), target)
        return respond

    def src_install(self, host, config_file):
        if not os.path.exists(config_file):
            raise Exception("Can not found the config file.")
        cfg = json.load(open(config_file))
        msg = self.chanl.make_msg("src_install", cfg=cfg)
        return self.chanl.call(msg, host, timeout=1000)

    def create_images(self, host, config_file):
        if not os.path.exists(config_file):
            raise Exception("Can not found the config file.")
        cfg = json.load(open(config_file))
        msg = self.chanl.make_msg("create_images", cfg=cfg)
        return self.chanl.call(msg, host, timeout=1000)

    def clean_images(self, host, config_file):
        if not os.path.exists(config_file):
            raise Exception("Can not found the config file.")
        cfg = json.load(open(config_file))
        msg = self.chanl.make_msg("clean_images", cfg=cfg)
        return self.chanl.call(msg, host, timeout=1000)

    def apply_model(self, host, model=None, config_file=None):
        if config_file is None:
            config_file = "/etc/vstf/env/%s.json" % model
        if not os.path.exists(config_file):
            raise Exception("Can not found the config file.")
        env = Builder(self.chanl, config_file)
        ret = env.build()
        return ret

    def disapply_model(self, host, model=None, config_file=None):
        if config_file is None:
            config_file = "/etc/vstf/env/%s.json" % model
        if not os.path.exists(config_file):
            raise Exception("Can not found the config file.")
        env = Builder(self.chanl, config_file)
        ret = env.clean()
        return ret

    def list_tasks(self):
        ret = self.dbconn.query_tasks()
        head = [["Task ID", "Task Name", "Task Date", "Task Remarks"]]
        if ret:
            ret = head + ret
        return ret

    def affctl_list(self, host):
        if not host:
            return "Need input the host"
        return Fabricant(host, self.chanl).affctl_list()

    def _create_task(self, scenario):
        taskid = self.dbconn.create_task(str(uuid.uuid4()), time.strftime(
            cst.TIME_FORMAT), desc=scenario + "Test")
        LOG.info("new Task id:%s" % taskid)
        if -1 == taskid:
            raise Exception("DB create task failed.")

        device = DeviceSettings().settings
        hosts = [device["host"], device["tester"]]
        for host in hosts:
            LOG.info(host)

            devs = host["devs"][0]
            keys = ["bdf", "iface", "mac"]
            key = devs.keys()[0]
            if key in keys:
                name = devs[key]
            else:
                raise Exception("error devs :%s", devs)

            query = Fabricant(host["agent"], self.chanl)
            nic_info = query.get_device_detail(identity=name)

            LOG.info(nic_info)

            os_info, cpu_info, mem_info, hw_info = self.collection.collect_host_info(host[
                                                                                     "agent"])
            LOG.info(os_info)
            LOG.info(cpu_info)
            LOG.info(mem_info)
            LOG.info(hw_info)

            self.dbconn.add_host_2task(taskid,
                                       host["agent"],
                                       json.dumps(hw_info[cst.HW_INFO]),
                                       json.dumps(cpu_info[cst.CPU_INFO]),
                                       json.dumps(mem_info[cst.MEMORY_INFO]),
                                       nic_info["desc"],
                                       json.dumps(os_info[cst.OS_INFO]))

        self.dbconn.add_extent_2task(taskid, "ixgbe", "driver", "")
        self.dbconn.add_extent_2task(taskid, "OVS", "switch", "")
        return taskid

    def settings(self, head, tail):

        forward_settings = ForwardingSettings()
        head_d = {
            "ip": head,
            "namespace": forward_settings.settings["head"]["namespace"]
        }
        tail_d = {
            "ip": tail,
            "namespace": forward_settings.settings["tail"]["namespace"]
        }
        LOG.info(head_d)
        LOG.info(tail_d)
        forward_settings.set_head(head_d)
        forward_settings.set_tail(tail_d)

    def report(self, rpath='./', mail_off=False, taskid=-1):
        report = rp.Report(self.dbconn, rpath)
        if taskid == -1:
            taskid = self.dbconn.get_last_taskid()
        report.report(taskid, mail_off)
        info_str = "do report over"
        return info_str

    def run_perf_cmd(
            self,
            case,
            rpath='./',
            affctl=False,
            build_on=False,
            save_on=False,
            report_on=False,
            mail_on=False):
        LOG.info(case)
        LOG.info(
            "build_on:%s report_on:%s mail_on:%s" %
            (build_on, report_on, mail_on))
        casetag = case['case']
        tool = case['tool']
        protocol = case['protocol']
        switch = "ovs"
        provider = None
        ttype = case['type']
        sizes = case['sizes']

        ret, ret_str = chk.check_case_params(protocol, ttype, tool)
        if not ret:
            return ret_str

        scenario = self.dbconn.query_scenario(casetag)
        LOG.info(scenario)
        if not scenario:
            LOG.warn("not support the case:%s", casetag)
            return

        config_file = os.path.join("/etc/vstf/env", scenario + ".json")

        LOG.info(config_file)
        env = Builder(self.chanl, config_file)
        if build_on:
            env.build()
        flows_settings = FlowsSettings()
        tool_settings = ToolSettings()
        tester_settings = TesterSettings()
        flow_producer = FlowsProducer(self.chanl, flows_settings)
        provider = PerfProvider(
            flows_settings.settings,
            tool_settings.settings,
            tester_settings.settings)

        perf = pf.Performance(self.chanl, provider)
        flow_producer.create(scenario, casetag)
        result = perf.run(tool, protocol, ttype, sizes, affctl)
        LOG.info(flows_settings.settings)
        LOG.info(result)
        if save_on:
            taskid = self._create_task(scenario)
            testid = self.dbconn.add_test_2task(
                taskid, casetag, protocol, ttype, switch, provider, tool)
            LOG.info(testid)
            self.dbconn.add_data_2test(testid, result)
            if report_on:
                self.report(rpath, not mail_on, taskid)
        return result

    def run_perf_file(
            self,
            rpath='./',
            affctl=False,
            report_on=True,
            mail_on=True):
        perf_settings = PerfSettings()
        flows_settings = FlowsSettings()
        tool_settings = ToolSettings()
        tester_settings = TesterSettings()
        flow_producer = FlowsProducer(self.chanl, flows_settings)
        provider = PerfProvider(
            flows_settings.settings,
            tool_settings.settings,
            tester_settings.settings)
        perf = pf.Performance(self.chanl, provider)
        tests = perf_settings.settings

        for scenario, cases in tests.items():
            LOG.info(scenario)
            if not cases:
                continue

            config_file = os.path.join("/etc/vstf/env", scenario + ".json")

            LOG.info(config_file)
            env = Builder(self.chanl, config_file)
            env.build()

            taskid = self._create_task(scenario)

            for case in cases:
                LOG.info(case)
                casetag = case['case']
                tool = case['tool']
                protocol = case['protocol']
                provider = None
                switch = "ovs"
                ttype = case['type']
                sizes = case['sizes']

                ret, ret_str = chk.check_case_params(protocol, ttype, tool)
                if not ret:
                    LOG.warn(ret_str)
                    continue

                flow_producer.create(scenario, casetag)
                result = perf.run(tool, protocol, ttype, sizes, affctl)
                LOG.info(result)

                testid = self.dbconn.add_test_2task(
                    taskid, casetag, protocol, ttype, switch, provider, tool)
                LOG.info(testid)

                self.dbconn.add_data_2test(testid, result)

            if report_on:
                self.report(rpath, not mail_on, taskid)

        info_str = "do batch perf test successfully"
        return info_str

    def collect_host_info(self, target):
        if self.collection is not None:
            return self.collection.collect_host_info(target)
        else:
            return "collection is None"


class Manager(daemon.Daemon):

    def __init__(self):
        """
        The manager will create a socket for vstfadm.
        also the manager own a ops chains
        """
        super(Manager, self).__init__(cst.vstf_pid)
        # the connection of socket
        self.conn = None
        # the operations of manager
        self.ops = None
        # record the daemon run flag
        self.run_flag = True

    def deal_unknown_obj(self, obj):
        return "unknown response %s:%s" % (self, obj)

    def run(self):
        signal.signal(signal.SIGTERM, self.daemon_die)
        # setup the socket server for communicating with vstfadm
        try:
            self.conn = unix.UdpServer()
            self.conn.bind()
            self.conn.listen()
        except Exception as e:
            raise e

        # accept the connection of vstfadm and recv the command
        # run the command from vstfadm and return the response
        while self.run_flag:
            conn, addr = self.conn.accept()
            LOG.debug("accept the conn: %(conn)s", {'conn': conn})

            # recv the msg until the conn break.

            while True:
                try:
                    data = message.recv(conn.recv)
                    LOG.debug("Manager recv the msg: %(msg)s", {'msg': data})
                    msg = message.decode(data)
                    body = message.get_body(msg)
                    context = message.get_context(msg)
                except RuntimeError:
                    LOG.debug("manage catch the connection close!")
                    break
                except Exception as e:
                    LOG.error("Manager recv message from socket failed.")
                    self.daemon_die()
                    raise e

                try:
                    func = getattr(self.ops, body.get('method'))
                    LOG.info("Call function:%s, args:%s",
                             func.__name__, body.get('args'))
                    response = func(**body.get('args'))
                    LOG.info("response: %s", response)
                except excepts.UnsolvableExit as e:
                    msg = "The manager opps, exit now"
                    LOG.error(msg)
                    # the manager has no need to be continue, just return
                    # this msg and exit normal
                    self.daemon_die()
                    raise e
                except Exception as e:
                    # here just the function failed no need exit, just return
                    # the msg
                    msg = "Run function failed. [ %s ]" % (e)
                    response = msg
                    LOG.error(msg)
                try:
                    response = message.add_context(response, **context)
                    LOG.debug(
                        "Manager send the response: <%(r)s", {
                            'r': response})
                    message.send(conn.send, message.encode(response))
                except Exception as e:
                    self.daemon_die()
                    raise e
            # close the connection when conn down
            conn.close()

    def daemon_die(self, signum, frame):
        """overwrite daemon.Daemon.daemon_die(self)"""
        LOG.info("manage catch the signal %s to exit." % signum)
        if self.conn:
            # we can not close the conn direct, just tell manager to stop
            # accept
            self.run_flag = False

        if self.ops:
            # stop the ops's proxy
            # maybe happen AttributeError: 'BlockingConnection' object has no attribute 'disconnect'
            # this a know bug in pika. fix in 0.9.14 release
            try:
                self.ops.chanl.close()
            except AttributeError:
                LOG.warning("The connection close happens attribute error")

    def start_manage(self, monitor="localhost", port=5672):
        try:
            # create manager's ops chains here will create a proxy to rabbitmq
            self.ops = OpsChains(monitor, port)
        except Exception as e:
            raise e
        self.start()

    def stop_manage(self):
        self.stop()


@cliutil.arg("--monitor",
             dest="monitor",
             default="localhost",
             action="store",
             help="which ip to be monitored")
@cliutil.arg("--port",
             dest="port",
             default="5672",
             action="store",
             help="rabbitmq conn server")
def do_start(args):
    Manager().start_manage(args.monitor, args.port)


def do_stop(args):
    Manager().stop_manage()


def main():
    """this is for vstfctl"""
    setup_logging(
        level=logging.INFO,
        log_file="/var/log/vstf/vstf-manager.log",
        clevel=logging.INFO)
    parser = VstfParser(
        prog="vstf-manager",
        description="vstf manager command line")
    parser.set_subcommand_parser(target=sys.modules[__name__])
    args = parser.parse_args()
    args.func(args)
