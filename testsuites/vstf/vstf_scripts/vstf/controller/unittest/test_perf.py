##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import unittest
import os
import logging

from vstf.controller.unittest import model
from vstf.controller.settings.flows_settings import FlowsSettings
from vstf.controller.settings.tool_settings import ToolSettings
from vstf.controller.settings.perf_settings import PerfSettings
from vstf.controller.sw_perf.perf_provider import PerfProvider
from vstf.controller.sw_perf.flow_producer import FlowsProducer
from vstf.controller.settings.tester_settings import TesterSettings
from vstf.controller.env_build.env_build import EnvBuildApi as Builder
from vstf.common.log import setup_logging
import vstf.controller.sw_perf.performance as pf

LOG = logging.getLogger(__name__)


class TestPerf(model.Test):

    def setUp(self):
        LOG.info("start performance unit test.")
        super(TestPerf, self).setUp()
        self.dir = os.path.dirname(__file__)
        self.perf_path = os.path.join(self.dir, '../../../etc/vstf/perf')
        self.base_path = os.path.join(self.dir, '../../../etc/vstf/env')

    def teardown(self):
        LOG.info("stop performance unit test.")

    @unittest.skip('for now')
    def test_batch_perf(self):

        LOG.info(self.perf_path)
        LOG.info(self.base_path)
        perf_settings = PerfSettings(path=self.perf_path)
        flows_settings = FlowsSettings(path=self.perf_path)
        tool_settings = ToolSettings(path=self.base_path)
        tester_settings = TesterSettings(path=self.base_path)
        flow_producer = FlowsProducer(self.conn, flows_settings)
        provider = PerfProvider(
            flows_settings.settings,
            tool_settings.settings,
            tester_settings.settings)
        perf = pf.Performance(self.conn, provider)
        tests = perf_settings.settings
        for scenario, cases in tests.items():
            if not cases:
                continue

            config_file = os.path.join(self.base_path, scenario + '.json')

            LOG.info(config_file)

            env = Builder(self.conn, config_file)
            env.build()

            for case in cases:
                casetag = case['case']
                tool = case['tool']
                protocol = case['protocol']
                profile = case['profile']
                ttype = case['type']
                sizes = case['sizes']

                flow_producer.create(scenario, casetag)
                result = perf.run(tool, protocol, ttype, sizes)
                self.assertEqual(True, isinstance(result, dict))
                LOG.info(result)

    @unittest.skip('for now')
    def test_perf_settings(self):
        perf_settings = PerfSettings()
        self.assertEqual(True, perf_settings.input())

    def test_tool_settings(self):
        tool_settings = ToolSettings()
        value = {
            "time": 20,
            "threads": 1
        }
        tool_settings.set_pktgen(value)
        tool_settings.set_netperf(value)
        tool_settings.set_iperf(value)
        tool_settings.set_qperf(value)
        LOG.info(tool_settings.settings)

    def test_flow_settings(self):
        tests = {
            "Tn": ["Tn-1", "Tn-2", "Tn-3", "Tn-4"],
            "Tnv": ["Tnv-1", "Tnv-2", "Tnv-3", "Tnv-4"],
            "Ti": ["Ti-1", "Ti-2", "Ti-3", "Ti-4", "Ti-5", "Ti-6"],
            "Tu": ["Tu-1", "Tu-2", "Tu-3", "Tu-4", "Tu-5", "Tu-6"]
        }
        flows_settings = FlowsSettings(path=self.perf_path)
        flow_producer = FlowsProducer(self.conn, flows_settings)

        for scenario, cases in tests.items():
            if not cases:
                continue

            config_file = os.path.join(self.base_path, scenario + '.json')

            LOG.info(config_file)

            env = Builder(self.conn, config_file)
            env.build()

            for case in cases:
                LOG.info(case)
                flow_producer.create(scenario, case)
                LOG.info(flows_settings.settings)


if __name__ == "__main__":
    setup_logging(
        level=logging.INFO,
        log_file="/var/log/vstf/vstf-unit-test.log",
        clevel=logging.INFO)
    unittest.main()
