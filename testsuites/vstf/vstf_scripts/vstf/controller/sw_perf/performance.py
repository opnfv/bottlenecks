##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import time
import argparse
import logging

from vstf.controller.sw_perf import model
from vstf.common import perfmark as mark
import vstf.common.constants as cst
import vstf.common.decorator as deco
from vstf.rpc_frame_work.rpc_producer import Server
from vstf.controller.settings.flows_settings import FlowsSettings
from vstf.controller.settings.tool_settings import ToolSettings
from vstf.controller.settings.perf_settings import PerfSettings
from vstf.controller.sw_perf.perf_provider import PerfProvider, get_agent_dict
from vstf.controller.sw_perf.flow_producer import FlowsProducer
from vstf.controller.settings.tester_settings import TesterSettings
from vstf.controller.fabricant import Fabricant

LOG = logging.getLogger(__name__)


class Performance(object):

    def __init__(self, conn, provider):
        self._provider = provider
        self._conn = conn
        self._init()

    def _init(self):
        self._senders = []
        self._receivers = []
        self._watchers = []
        self._cpuwatcher = None

    def create(self, tool, tpro):
        self._init()
        agents = self._provider.get_cleaners(tool, tpro)
        LOG.info(agents)
        for agent in agents:
            cleaner = Fabricant(agent, self._conn)
            cleaner.clean_all_namespace()

        for tester_info in self._provider.get_testers:
            dst = tester_info["agent"]
            params = tester_info["params"]
            LOG.info(tester_info)
            driver_mgr = Fabricant(dst, self._conn)
            ret = driver_mgr.install_drivers(drivers=params["drivers"])
            LOG.info(ret)

        self.create_namespace(tool)
        self.create_senders(tool, tpro)
        self.create_receivers(tool, tpro)
        self.create_watchers(tool)
        self.create_cpuwatcher()

    def destory(self, tool):
        self.clear_namespace(tool)

    def create_namespace(self, tool):
        devices = self._provider.get_namespaces(tool)
        agents = get_agent_dict(devices)
        LOG.info(agents)
        for device in devices:
            dst = device["agent"]
            params = device["params"]
            if not agents[dst]:
                model.NetDeviceMgr.clear(dst, self._conn)
                agents[dst] = True

            model.NetDeviceMgr.add(dst, self._conn, params)

    def clear_namespace(self, tool):
        devices = self._provider.get_namespaces(tool)
        for device in devices:
            dst = device["agent"]
            params = device["params"]
            model.NetDeviceMgr.remove(dst, self._conn, params)

    def create_senders(self, tool, tpro):
        sender_infos = self._provider.get_senders(tool, tpro)
        LOG.info(sender_infos)
        for sender_info in sender_infos:
            dst = sender_info["agent"]
            params = sender_info["params"]
            send = model.Sender(dst, self._conn, tool, params)
            self._senders.append(send)

    def create_receivers(self, tool, tpro):
        receiver_infos = self._provider.get_receivers(tool, tpro)
        LOG.info(receiver_infos)
        for receiver_info in receiver_infos:
            dst = receiver_info["agent"]
            params = receiver_info["params"]
            receive = model.Receiver(dst, self._conn, tool, params)
            self._receivers.append(receive)

    def create_watchers(self, tool):
        watcher_infos = self._provider.get_watchers(tool)
        LOG.info(watcher_infos)
        for watcher_info in watcher_infos:
            dst = watcher_info["agent"]
            params = watcher_info["params"]
            watch = model.NicWatcher(dst, self._conn, params)
            self._watchers.append(watch)

    def create_cpuwatcher(self):
        watcher_info = self._provider.get_cpuwatcher
        LOG.info(watcher_info)
        dst = watcher_info["agent"]
        self._cpuwatcher = model.CpuWatcher(dst, self._conn)

    def start_receivers(self, **kwargs):
        for receiver in self._receivers:
            receiver.start(**kwargs)

    def start_senders(self, pktsize, **kwargs):
        for sender in self._senders:
            sender.start(pktsize, **kwargs)

    def start_watchers(self):
        for watcher in self._watchers:
            watcher.start()

    def stop_receivers(self):
        for receiver in self._receivers:
            receiver.stop()

    def stop_senders(self):
        for sender in self._senders:
            sender.stop()

    def stop_watchers(self):
        for watcher in self._watchers:
            watcher.stop()

    def start_cpuwatcher(self, enable=True):
        if self._cpuwatcher and enable:
            self._cpuwatcher.start()

    def stop_cpuwatcher(self, enable=True):
        if self._cpuwatcher and enable:
            self._cpuwatcher.stop()

    def getlimitspeed(self, ptype, size):
        return 0

    def affctl(self):
        ctl = self._provider.get_cpu_affctl
        LOG.info(ctl)
        driver_mgr = Fabricant(ctl["agent"], self._conn)
        ret = driver_mgr.affctl_load(policy=ctl["params"]["policy"])
        LOG.info(ret)

    def run_pre_affability_settings(self, tool, tpro, pktsize, **kwargs):
        LOG.info("run_pre_affability_settings start")
        self.create(tool, tpro)
        self.start_receivers()
        self.start_senders(pktsize, **kwargs)
        self.affctl()
        time.sleep(2)
        self.stop_senders()
        self.stop_receivers()
        self.destory(tool)
        LOG.info("run_pre_affability_settings end")

    @deco.check("ratep", defaults=0)
    @deco.check("cpu_watch", defaults=False)
    def run_bandwidth_test(self, tool, tpro, pktsize, **kwargs):
        LOG.info("run_bandwidth_test ")
        cpu_watch = kwargs.pop("cpu_watch")
        self.create(tool, tpro)
        self.start_receivers()
        self.start_senders(pktsize, **kwargs)
        time.sleep(self._provider.wait_balance(tool))
        self.start_watchers()
        self.start_cpuwatcher(cpu_watch)
        time.sleep(self._provider.duration(tool))
        self.stop_watchers()
        self.stop_cpuwatcher(cpu_watch)
        self.stop_senders()
        self.stop_receivers()
        self.destory(tool)
        LOG.info("run_bandwidth_test end")

    @deco.check("ratep", defaults=0)
    def run_latency_test(self, tool, tpro, pktsize, **kwargs):
        LOG.info("run_latency_test start")
        self.create(tool, tpro)
        self.start_receivers()
        self.start_senders(pktsize, **kwargs)
        time.sleep(self._provider.duration(tool))
        self.stop_senders()
        self.stop_receivers()
        self.destory(tool)
        LOG.info("run_latency_test end")

    def run(self, tool, protocol, ttype, sizes, affctl=False):
        result = {}
        if affctl:
            pre_tpro = protocol + "_bw"
            size = sizes[0]
            self.run_pre_affability_settings(tool, pre_tpro, size, ratep=0)

        for size in sizes:
            if ttype in ['throughput', 'frameloss']:
                realspeed = self.getlimitspeed(ttype, size)
                bw_tpro = protocol + "_bw"
                bw_type = ttype
                self.run_bandwidth_test(tool, bw_tpro, size, ratep=realspeed)
                bw_result = self.result(tool, bw_type)

                lat_tool = "qperf"
                lat_type = 'latency'
                lat_tpro = protocol + '_lat'
                self.run_latency_test(
                    lat_tool, lat_tpro, size, ratep=realspeed)
                lat_result = self.result(tool, lat_type)
                LOG.info(bw_result)
                LOG.info(lat_result)
                lat_result.pop('OfferedLoad')
                bw_result.update(lat_result)
                result[size] = bw_result

            elif ttype in ['latency']:
                lat_tpro = protocol + '_lat'
                lat_type = ttype
                self.run_latency_test(tool, lat_tpro, size, ratep=0)
                lat_result = self.result(tool, lat_type)
                result[size] = lat_result
            else:
                raise Exception("error:protocol type:%s" % (ttype))
        return result

    def result(self, tool, ttype):
        if ttype in {'throughput', 'frameloss'}:
            record = {
                mark.rxCount: 0,
                mark.txCount: 0,
                mark.bandwidth: 0,
                mark.offLoad: 100.0,
                mark.mppsGhz: 0,
                mark.percentLoss: 0,
                mark.avgLatency: 0,
                mark.maxLatency: 0,
                mark.minLatency: 0,
                mark.rxMbps: 0,
                mark.txMbps: 0
            }

            cpu_data = self._cpuwatcher.result()
            print self._cpuwatcher, cpu_data
            if cpu_data:
                cpu_usage = cpu_data['cpu_num'] * (100 - cpu_data['idle'])
                cpu_mhz = cpu_data['cpu_mhz']
                record[mark.cpu] = round(cpu_usage, cst.CPU_USAGE_ROUND)
                record[mark.duration] = self._provider.duration(tool)

            for watcher in self._watchers:
                nic_data = watcher.result()
                record[mark.rxCount] += nic_data['rxpck']
                record[mark.txCount] += nic_data['txpck']
                record[mark.bandwidth] += nic_data['rxpck/s']
                record[mark.rxMbps] += nic_data['rxmB/s'] * 8
                record[mark.txMbps] += nic_data['txmB/s'] * 8

            if record[mark.rxMbps] > record[mark.txMbps]:
                record[
                    mark.rxMbps], record[
                    mark.txMbps] = record[
                    mark.txMbps], record[
                    mark.rxMbps]

            if record[mark.rxCount] > record[mark.txCount]:
                record[
                    mark.rxCount], record[
                    mark.txCount] = record[
                    mark.txCount], record[
                    mark.rxCount]

            if record[mark.txCount]:
                record[mark.percentLoss] = round(
                    100 * (1 - record[mark.rxCount] / record[mark.txCount]), cst.PKTLOSS_ROUND)
            else:
                record[mark.percentLoss] = 100

            record[mark.bandwidth] /= 1000000.0
            if cpu_mhz and record[mark.cpu]:
                record[mark.mppsGhz] = round(
                    record[mark.bandwidth] / (record[mark.cpu] * cpu_mhz / 100000), cst.CPU_USAGE_ROUND)

            record[mark.bandwidth] = round(
                record[mark.bandwidth], cst.RATEP_ROUND)

        elif ttype in {'latency'}:
            record = {
                mark.offLoad: 0.0,
                mark.avgLatency: 0,
                mark.maxLatency: 0,
                mark.minLatency: 0
            }
            minlatency, avglatency, maxlatency = 0, 0, 0
            count = 0
            for sender in self._senders:
                info = sender.result()
                LOG.info(info)
                minlatency += info[mark.minLatency]
                avglatency += info[mark.avgLatency]
                maxlatency += info[mark.maxLatency]
            count = 1 if not count else count
            record[mark.minLatency] = round(minlatency / count, cst.TIME_ROUND)
            record[mark.avgLatency] = round(avglatency / count, cst.TIME_ROUND)
            record[mark.maxLatency] = round(maxlatency / count, cst.TIME_ROUND)

        else:
            raise Exception('error:protocol type:%s' % ttype)

        LOG.info('record:%s' % record)
        return record


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-sw_perf.log",
        clevel=logging.INFO)

    conn = Server("192.168.188.10")
    perf_settings = PerfSettings()
    flows_settings = FlowsSettings()
    tool_settings = ToolSettings()
    tester_settings = TesterSettings()
    flow_producer = FlowsProducer(conn, flows_settings)
    provider = PerfProvider(
        flows_settings.settings,
        tool_settings.settings,
        tester_settings.settings)
    perf = Performance(conn, provider)
    tests = perf_settings.settings
    for scenario, cases in tests.items():
        if not cases:
            continue
        for case in cases:
            casetag = case['case']
            tool = case['tool']
            protocol = case['protocol']
            profile = case['profile']
            ttype = case['type']
            sizes = case['sizes']

            flow_producer.create(scenario, casetag)
            result = perf.run(tool, protocol, ttype, sizes)
            LOG.info(result)


def main():
    from vstf.common.log import setup_logging
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-performance.log",
        clevel=logging.INFO)
    from vstf.controller.database.dbinterface import DbManage
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("case",
                        action="store",
                        help="test case like Ti-1, Tn-1, Tnv-1, Tu-1...")
    parser.add_argument("tool",
                        action="store",
                        choices=cst.TOOLS,
                        )
    parser.add_argument("protocol",
                        action="store",
                        choices=cst.TPROTOCOLS,
                        )
    parser.add_argument("profile",
                        action="store",
                        choices=cst.PROVIDERS,
                        )
    parser.add_argument("type",
                        action="store",
                        choices=cst.TTYPES,
                        )
    parser.add_argument("sizes",
                        action="store",
                        default="64",
                        help='test size list "64 128"')
    parser.add_argument(
        "--affctl",
        action="store_true",
        help="when input '--affctl', the performance will do affctl before testing")
    parser.add_argument("--monitor",
                        dest="monitor",
                        default="localhost",
                        action="store",
                        help="which ip to be monitored")
    args = parser.parse_args()

    LOG.info(args.monitor)
    conn = Server(host=args.monitor)
    db_mgr = DbManage()

    casetag = args.case
    tool = args.tool
    protocol = args.protocol
    profile = args.profile
    ttype = args.type
    sizes = map(lambda x: int(x), args.sizes.strip().split())

    flows_settings = FlowsSettings()
    tool_settings = ToolSettings()
    tester_settings = TesterSettings()
    flow_producer = FlowsProducer(conn, flows_settings)
    provider = PerfProvider(
        flows_settings.settings,
        tool_settings.settings,
        tester_settings.settings)
    perf = Performance(conn, provider)
    scenario = db_mgr.query_scenario(casetag)
    flow_producer.create(scenario, casetag)
    LOG.info(flows_settings.settings)
    result = perf.run(tool, protocol, ttype, sizes, affctl)


if __name__ == '__main__':
    main()
