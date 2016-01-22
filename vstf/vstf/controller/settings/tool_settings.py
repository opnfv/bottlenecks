##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import logging
import pprint
import vstf.controller.settings.settings as sets
import vstf.common.decorator as deco
from vstf.common.input import raw_choice

LOG = logging.getLogger(__name__)


class ToolSettings(sets.Settings):
    def __init__(self, path="/etc/vstf", filename="sw_perf.tool-settings", mode=sets.SETS_DEFAULT):
        super(ToolSettings, self).__init__(path, filename, mode)

    def _register_func(self):
        body = set(
            self._fset.keys()
        )
        LOG.debug(body)
        for item in body:
            item = item.encode()
            func_name = "set_%s" % (item)
            setattr(self, func_name,
                    self._setting_file(func_name, self._mset, self._fset, item, check=self._check_keys))

    def _check_keys(self, value):
        keys = ['threads', 'wait', 'time']
        if not isinstance(value, dict):
            raise Exception("type is error: %s" % (str(value)))
        for key in keys:
            if key not in value.keys():
                raise Exception("keys[%s] is missing: %s" % (key, str(value)))

    def sinput(self):
        body = set(
            self._fset.keys()
        )
        for tool in body:
            info = "if set %s properties" % tool
            if raw_choice(info):
                properties = self.raw_properties()
                func = getattr(self, "set_%s" % tool)
                func(properties)

        print "%s set finish: " % self._filename
        print "+++++++++++++++++++++++++++++++++++++++++"
        pprint.pprint(self.settings, indent=4)
        print "+++++++++++++++++++++++++++++++++++++++++"

    @deco.vstf_input("time", types=int)
    @deco.vstf_input("wait", types=int)
    @deco.vstf_input("threads", types=int)
    def raw_properties(self):
        print "---------------------------------------"
        print "Please vstf set tool properties like:"
        print "    'threads': 2,"
        print "    'wait': 2,"
        print "    'time': 10,"
        print "---------------------------------------"


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf/tool-settings.log", clevel=logging.INFO)
    tool_settings = ToolSettings()
    value = {
        "time": 10,
        "wait": 4,
        "threads": 1
    }
    tool_settings.set_pktgen(value)
    tool_settings.set_netperf(value)
    tool_settings.set_iperf(value)
    tool_settings.set_qperf(value)
    LOG.info(tool_settings.settings)


if __name__ == '__main__':
    unit_test()
