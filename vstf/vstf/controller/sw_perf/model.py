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
from vstf.controller.sw_perf.raw_data import RawDataProcess
from vstf.common import perfmark as mark

LOG = logging.getLogger(__name__)


class NetDeviceMgr(Fabricant):
    @classmethod
    def add(cls, dst, conn, dev):
        self = cls(dst, conn)
        LOG.info(dev)
        ret = self.config_dev(netdev=dev)
        LOG.info(ret)

    @classmethod
    def remove(cls, dst, conn, dev):
        self = cls(dst, conn)
        LOG.info(dev)
        ret = self.recover_dev(netdev=dev)
        LOG.info(ret)

    @classmethod
    def clear(cls, dst, conn):
        self = cls(dst, conn)
        self.clean_all_namespace()


class Actor(Fabricant):
    def __init__(self, dst, conn, tool, params):
        super(Actor, self).__init__(dst, conn)
        self._tool = tool
        self._params = params
        self._data = {}

    def __repr__(self):
        repr_dict = self.__dict__
        repr_keys = list(repr_dict.keys())
        repr_keys.sort()
        return '%s(%s)' % (self.__class__.__name__, ', '.join(['%s=%r' % (k, repr_dict[k]) for k in repr_keys]))


class Sender(Actor):
    def start(self, pktsize, **kwargs):
        LOG.info("Sender.start")
        if 'ratep' in kwargs and kwargs['ratep']:
            self._params['ratep'] = kwargs['ratep']
        self._params['size'] = pktsize

        ret, info = self.perf_run(
            operation="start",
            action="send",
            tool=self._tool,
            params=self._params
        )
        LOG.info(ret)
        if ret:
            raise Exception(info)
        LOG.info(info)
        print ret

    def stop(self):
        LOG.info(self._params)
        rets = self.perf_run(
            operation="stop",
            action="send",
            tool=self._tool,
            params={}
        )
        LOG.info(rets)
        minlatency, avglatency, maxlatency = 0, 0, 0
        count = 0
        for (ret, info) in rets:
            if ret:
                raise Exception(info)
            if self.is_data() and ret == 0:
                count += 1
                minlatency += info[mark.minLatency]
                avglatency += info[mark.avgLatency]
                maxlatency += info[mark.maxLatency]
        count = 1 if not count else count
        self._data[mark.minLatency] = minlatency / count
        self._data[mark.avgLatency] = avglatency / count
        self._data[mark.maxLatency] = maxlatency / count

        print rets

    def is_data(self):
        if '_lat' in self._params['protocol']:
            return True
        return False

    def result(self):
        return self._data


class Receiver(Actor):
    def start(self, **kwargs):
        LOG.info("Receiver.start")
        ret, info = self.perf_run(
            operation="start",
            action="receive",
            tool=self._tool,
            params=self._params
        )
        LOG.info(ret)
        if ret:
            raise Exception(info)
        LOG.info(info)
        return ret

    def stop(self):
        LOG.info("Receiver.stop")
        ret, info = self.perf_run(
            operation="stop",
            action="receive",
            tool=self._tool,
            params=self._params
        )
        LOG.info(ret)
        if ret:
            raise Exception(info)
        LOG.info(info)
        return ret


class NicWatcher(Fabricant):
    def __init__(self, dst, conn, params):
        super(NicWatcher, self).__init__(dst, conn)
        self._params = params
        self._pid = None
        self._data = {}

    def start(self):
        print "NicWatcher.start"
        self._pid = self.run_vnstat(device=self._params["iface"], namespace=self._params["namespace"])
        print self._pid

    def stop(self):
        print "NicWatcher.stop"
        if self._pid:
            data = self.kill_vnstat(pid=self._pid)
            self._data = RawDataProcess.process(data)
            print "---------------------------------"
            print self._data
            print "---------------------------------"

    def result(self, **kwargs):
        return self._data


class CpuWatcher(Fabricant):
    def __init__(self, dst, conn):
        super(CpuWatcher, self).__init__(dst, conn)
        self._pid = None
        self._data = {
            "cpu_num": 0,
            "idle": 0,
            "cpu_mhz": 0
        }

    def start(self):
        print "CpuWatcher.start"
        self._pid = self.run_cpuwatch()
        print self._pid

    def stop(self):
        print "CpuWatcher.stop"
        if self._pid:
            print self._pid
            data = self.kill_cpuwatch(pid=self._pid)
            self._data = RawDataProcess.process(data)
            print "---------------------------------"
            print self._data
            print "---------------------------------"

    def result(self, **kwargs):
        return self._data


def unit_test():
    pass


if __name__ == '__main__':
    unit_test()
