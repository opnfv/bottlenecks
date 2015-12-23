#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-11-19
# see license for license details

import logging

from vstf.controller.settings.device_settings import DeviceSettings
from vstf.controller.settings.forwarding_settings import ForwardingSettings
from vstf.controller.settings.cpu_settings import CpuSettings
from vstf.controller.fabricant import Fabricant
from vstf.controller.settings.flows_settings import FlowsSettings
import vstf.common.constants as cst

LOG = logging.getLogger(__name__)


class FlowsProducer(object):
    def __init__(self, conn, flows_settings):
        self._perf = flows_settings
        self._forwarding = ForwardingSettings().settings
        self._device = DeviceSettings().settings
        self._cpu = CpuSettings().settings
        self._conn = conn
        self._devs_map = {}

    def get_dev(self, item):
        agent = self._device[item[0]]["agent"]
        devs = self._device[item[0]]["devs"][item[1]]

        keys = ["bdf", "iface", "mac"]

        key = devs.keys()[0]

        if key in keys:
            name = devs[key]
        else:
            raise Exception("error devs :%s", devs)
        LOG.info(agent)
        LOG.info(name)
        if not self._devs_map.has_key((agent, name)):
            query = Fabricant(agent, self._conn)
            query.clean_all_namespace()
            dev_info = query.get_device_verbose(identity=name)
            if not isinstance(dev_info, dict):
                err = "get device detail failed, agent:%s net:%s" % (agent, name)
                raise Exception(err)
            dev = {
                "agent": agent,
                "dev": {
                    "bdf": dev_info["bdf"],
                    "iface": dev_info["iface"],
                    "mac": dev_info["mac"],
                    "ip": None,
                    "namespace": None
                }
            }

            self._devs_map[(agent, name)] = dev
            LOG.info(dev)

        return self._devs_map[(agent, name)]

    def get_host(self):
        result = {
            "agent": self._device["host"]["agent"],
            "affctl": self._cpu["affctl"]
        }
        return result

    def create(self, scenario, case):
        self._devs_map = {}
        flows_indexes = self._forwarding[scenario]["flows"]
        flows_infos = []
        for index in flows_indexes:
            if not index:
                raise Exception("error flows %s" % flows_indexes)
            dev = self.get_dev(index)
            flows_infos.append(dev)

        flows_infos[0]['dev'].update(self._forwarding["head"])
        flows_infos[-1]['dev'].update(self._forwarding["tail"])

        LOG.info(flows_infos)

        actor_info = cst.CASE_ACTOR_MAP[case]

        self._perf.clear_all()
        senders = actor_info["senders"]
        LOG.info(senders)
        for sender in senders:
            dev = flows_infos[sender]
            if dev:
                self._perf.add_senders(dev)

        receivers = actor_info["receivers"]
        for receiver in receivers:
            dev = flows_infos[receiver]
            if dev:
                self._perf.add_receivers(dev)

        watchers = self._forwarding[scenario]["watchers"]
        for watcher in watchers:
            dev = flows_infos[watcher]
            if dev:
                self._perf.add_watchers(dev)

        namespaces = [0, -1]
        for namespace in namespaces:
            dev = flows_infos[namespace]
            if dev:
                self._perf.add_namespaces(dev)

        host = self.get_host()
        if host:
            self._perf.add_cpu_listens(host)

        self._perf.set_flows(actor_info["flows"])
        return True


def unit_test():
    from vstf.rpc_frame_work.rpc_producer import Server
    from vstf.common.log import setup_logging
    setup_logging(level=logging.INFO, log_file="/var/log/vstf/vstf-producer.log", clevel=logging.INFO)

    conn = Server("192.168.188.10")
    flow_settings = FlowsSettings()
    flow_producer = FlowsProducer(conn, flow_settings)
    scenario = "Tn"
    case = "Tn-1"
    flow_producer.create(scenario, case)


if __name__ == '__main__':
    unit_test()
