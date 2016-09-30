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


class CpuSettings(sets.Settings):

    def __init__(self, path="/etc/vstf/perf/",
                 filename="sw_perf.cpu-settings",
                 mode=sets.SETS_SINGLE):
        super(CpuSettings, self).__init__(path, filename, mode)

    def _register_func(self):
        super(CpuSettings, self)._register_func()
        body = set(
            self._fset['affctl'].keys()
        )
        LOG.debug(body)
        for item in body:
            item = item.encode()
            func_name = "set_%s" % item
            setattr(
                self,
                func_name,
                self._setting_file(
                    func_name,
                    self._mset['affctl'],
                    self._fset['affctl'],
                    item))
            func_name = "mset_%s" % item
            setattr(
                self,
                func_name,
                self._setting_memory(
                    func_name,
                    self._mset['affctl'],
                    item))

        LOG.debug(self.__dict__)

    def sinput(self, info=None):
        if raw_choice("if set cpu affability by affctl"):
            affctl = self.raw_affctl(info)
            self.set_affctl(affctl)

        print "%s set finish: " % self._filename
        print "+++++++++++++++++++++++++++++++++++++++++"
        pprint.pprint(self.settings, indent=4)
        print "+++++++++++++++++++++++++++++++++++++++++"

    @deco.vstf_input('policy', types=int)
    def raw_affctl(self, info):
        print info
        print "---------------------------------------"
        print "Please vstf set cpu affctl params like:"
        print "    'policy': 2,"
        print "---------------------------------------"


def unit_test():
    from vstf.common.log import setup_logging
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-cpu-settings.log",
        clevel=logging.INFO)

if __name__ == '__main__':
    unit_test()
