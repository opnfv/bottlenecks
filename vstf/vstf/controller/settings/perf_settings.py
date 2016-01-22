##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pprint
import logging

import vstf.common.decorator as deco
import vstf.common.constants as cst
import vstf.controller.settings.settings as sets
from vstf.common.input import raw_choice
from vstf.controller.database.dbinterface import DbManage

LOG = logging.getLogger(__name__)


class PerfSettings(sets.Settings):
    def __init__(self, path="/etc/vstf/perf/",
                 filename="sw_perf.batch-settings",
                 mode=sets.SETS_SINGLE):
        self.dbconn = DbManage()
        super(PerfSettings, self).__init__(path, filename, mode)

    def clear(self):
        for item in cst.SCENARIOS:
            func = getattr(self, "set_" + item)
            func([])

    def mclear(self):
        for item in cst.SCENARIOS:
            func = getattr(self, "mset_" + item)
            func([])

    def add_case(self, value):
        scenario = self.dbconn.query_scenario(value["case"])
        LOG.info(scenario)
        if not scenario:
            LOG.warn("not support the case:%s", value["case"])
            return
        self._adding_file("add", self._mset, self._fset, scenario, check=self._check_add)(value)

    def madd_case(self, case):
        scenario = self.dbconn.query_scenario(case)
        if not scenario:
            LOG.warn("not support the case:%s", case)
            return
        self._adding_memory("madd", self._mset, scenario, check=self._check_add)(case)

    @deco.dcheck('sizes')
    @deco.dcheck("type", choices=cst.TTYPES)
    @deco.dcheck("profile", choices=cst.PROVIDERS)
    @deco.dcheck("protocol", choices=cst.TPROTOCOLS)
    @deco.dcheck("tool", choices=cst.TOOLS)
    @deco.dcheck('case')
    def _check_add(self, value):
        LOG.info("check successfully")

    def sinput(self):
        if raw_choice("if clean all Test case"):
            self.clear()
        while True:
            if raw_choice("if add a new Test case"):
                case = self.raw_addcase()
                self.add_case(case)
            else:
                break
        print "%s set finish: " % (self._filename)
        print "+++++++++++++++++++++++++++++++++++"
        pprint.pprint(self.settings)
        print "+++++++++++++++++++++++++++++++++++"
        return True
    
    @deco.vstf_input('sizes', types=list)
    @deco.vstf_input("type", types=str, choices=cst.TTYPES)
    @deco.vstf_input("profile", types=str, choices=cst.PROVIDERS)
    @deco.vstf_input("protocol", types=str, choices=cst.TPROTOCOLS)
    @deco.vstf_input("tool", types=str, choices=cst.TOOLS)
    @deco.vstf_input('case')
    def raw_addcase(self):
        print "---------------------------------------"
        print "Please vstf add case info like:"
        print "    'case': 'Ti-1',"
        print "    'tool': 'netperf',"
        print "    'protocol': 'udp',"
        print "    'profile': 'rdp',"
        print "    'type': 'latency',"
        print "    'sizes': [64, 128, 512, 1024]"
        print "---------------------------------------"


def unit_test():
    perf_settings = PerfSettings()
    perf_settings.sinput()

    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf/vstf-perf-settings.log", clevel=logging.DEBUG)


if __name__ == '__main__':
    unit_test()
