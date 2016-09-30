##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import subprocess
import time
import logging
import vstf.agent.perf.utils as utils
import vstf.common.decorator as deco
from vstf.common.utils import my_popen

LOG = logging.getLogger(__name__)


class Pktgen(object):

    def __init__(self):
        utils.modprobe_pktgen()
        self._send_processes = []

    def _psetpg(self, dev):
        self._dev = dev

    def _vsetpg(self, key, value=''):
        with open(self._dev, 'w') as f:
            txt = "%(key)s %(value)s\n" % {'key': key, 'value': value}
            f.write(txt)
            LOG.info("write(%s) to %s", txt.strip(), self._dev)

    def _start(self):
        cmd = 'echo start > /proc/net/pktgen/pgctrl'
        process = my_popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        LOG.info('running pid:%s', process.pid)
        time.sleep(0.5)
        ret = process.poll()
        if ret is None:
            ret = 0
            self._send_processes.append(process)
            error_str = "start pktgen send success"
        else:
            error_str = "start pktgen send failed, stdout:%s,stderr:%s" % (
                process.stdout.read(), process.stderr.read())
            LOG.info(error_str)
        return ret, error_str

    def _rem_device_all(self):
        cpu_num = utils.get_cpu_num()
        for thread in range(0, cpu_num - 1):
            self._psetpg("/proc/net/pktgen/kpktgend_%s" % thread)
            self._vsetpg('rem_device_all')
        return True

    @deco.check("protocol", choices=['udp_bw'], defaults='udp_bw')
    @deco.check("namespace", defaults=None)
    @deco.check("dst")
    @deco.check("src")
    @deco.check("size", defaults=64)
    @deco.check("threads", defaults=utils.get_default_threads())
    @deco.check("clone_skb", defaults=1)
    @deco.check("count", defaults=0)
    @deco.check("ratep", defaults=0)
    def send_start(self, **kwargs):
        # ensure that all sends is exit
        self.send_stop()

        interface_num = len(kwargs['src'])
        interfaces = []
        for i in range(interface_num):
            device = kwargs['src'][i]['iface']
            interfaces.append(device)
            utils.iface_up(device)

        self._rem_device_all()

        threads = kwargs['threads']
        for i in range(interface_num):
            dev_min = i * threads
            dev_max = (i + 1) * threads
            device = interfaces[i]
            for dev_id in range(dev_min, dev_max):
                queue_id = dev_id % threads
                self._psetpg("/proc/net/pktgen/kpktgend_%s" % dev_id)
                self._vsetpg('add_device', "%s@%s" % (device, queue_id))
                self._psetpg("/proc/net/pktgen/%s@%s" % (device, queue_id))
                self._vsetpg('pkt_size', kwargs['size'])
                self._vsetpg('clone_skb', kwargs['clone_skb'])
                self._vsetpg('dst_mac', kwargs['dst'][i]['mac'])
                self._vsetpg('src_mac', kwargs['src'][i]['mac'])
                self._vsetpg('count', kwargs['count'])
                if kwargs['ratep']:
                    self._vsetpg('ratep', kwargs['ratep'])
        return self._start()

    def send_stop(self, **kwargs):
        results = []
        ret = 0
        for process in self._send_processes:
            process.kill()
            process.wait()
            LOG.info("process.kill(pktgen:%s)", process.pid)
            results.append((ret, process.stdout.read()))
        self._send_processes = []
        return results

    def receive_start(self, **kwargs):
        ret = 0
        error_str = "%s pktgen neednt receive start" % (self.__class__)
        LOG.debug(error_str)
        return ret, error_str

    def receive_stop(self, **kwargs):
        ret = 0
        error_str = "pktgen neednt receive stop"
        LOG.debug(error_str)
        return ret, error_str

    def clean(self):
        self.send_stop()
        return True

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        return self.clean()


def unit_test():
    perf = Pktgen()
    print perf.receive_start()
    send = {
        "src": [
            {"iface": 'eth4', "mac": "90:e2:ba:20:1f:d8"}
        ],
        "dst": [
            {"mac": '90:e2:ba:20:1f:d9'}
        ],
        "size": 64,
        "threads": 1,
        'ratep': 0
    }
    print perf.send_start(**send)
    time.sleep(30)
    print perf.send_stop()
    print perf.receive_stop()


if __name__ == "__main__":
    from vstf.common.log import setup_logging

    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-pktgen.log",
        clevel=logging.DEBUG)
    unit_test()
