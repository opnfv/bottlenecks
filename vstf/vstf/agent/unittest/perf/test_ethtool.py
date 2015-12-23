#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015/11/13
# see license for license details

import unittest
import logging
from vstf.agent.perf import ethtool
from vstf.agent.unittest import configuration
from vstf.common.log import setup_logging


LOG = logging.getLogger(__name__)


class Testethtool(unittest.TestCase):
    def setUp(self):
        LOG.info("start Testethtool unit test.")
        self._devices = configuration.eth_for_test
        super(Testethtool, self).setUp()

    def teardown(self):
        LOG.info("stop Testethtool unit test.")

#    @unittest.skip('for now')
    def test_autoneg_on(self):
        for dev in self._devices:
            self.assertTrue(ethtool.autoneg_on(dev), True)

    def test_autoneg_off(self):
        for dev in self._devices:
            self.assertTrue(ethtool.autoneg_off(dev), True)

    def test_autoneg_query(self):
        for dev in self._devices:
            result = ethtool.autoneg_query(dev)
            LOG.info(result)

if __name__ == "__main__":
    setup_logging(level=logging.INFO, log_file="/var/log/vstf/vstf-unit-test.log", clevel=logging.INFO)
    unittest.main()
