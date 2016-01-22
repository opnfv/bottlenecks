##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import time
import subprocess
import vstf.common.decorator as deco
from vstf.common.utils import kill_by_name, my_popen

import logging

LOG = logging.getLogger(__name__)


class Netmap(object):
    def __init__(self):
        self._send_processes = []
        self._receive_processes = []

    @deco.check("protocol", choices=['udp_bw'], defaults='udp_bw')
    @deco.check("namespace", defaults=None)
    @deco.check("dst")
    @deco.check("src")
    @deco.check("size", defaults=64)
    @deco.check("threads", defaults=1)
    @deco.check("ratep", defaults=0)
    def send_start(self, **kwargs):
        cmd = self.format_send_start(**kwargs)
        LOG.info("cmd:%s", cmd)

        process = my_popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._send_processes.append(process)
        time.sleep(0.5)

        ret = process.poll()
        if ret is None:
            ret = 0
            error_str = "start netmap send success"
        else:
            error_str = "start netmap send failed, %s" % (str(kwargs))
            process.wait()
            self._send_processes.remove(process)

        return ret, error_str

    def send_stop(self, **kwargs):
        LOG.info("send_stop")
        results = []
        ret = 0
        for process in self._send_processes:
            process.kill()
            process.wait()
            error_str = "stop netmap send success"
            results.append((ret, error_str))
        self._send_processes = []
        return results

    def format_send_start(self, **kwargs):
        cmd = "pkt-gen -i %(src_iface)s -f tx -l %(pkt_size)s -p %(threads)s -D %(dst_mac)s -R %(ratep)s"
        context = {
            'src_iface': kwargs['src'][0]['iface'],
            'dst_mac': kwargs['dst'][0]['mac'],
            'pkt_size': kwargs['size'],
            'threads': kwargs['threads'],
            'ratep': kwargs['ratep']
        }
        cmd = cmd % context
        return cmd

    @deco.namespace()
    def format_receive_start(self, **kwargs):
        cmd = "pkt-gen -i %(iface)s -f rx"
        context = {
            'iface': kwargs['dst'][0]['iface']
        }
        cmd = cmd % context
        return cmd

    @deco.check("protocol", choices=['udp_bw'], defaults='udp_bw')
    @deco.check("namespace", defaults=None)
    @deco.check("dst")
    def receive_start(self, **kwargs):

        cmd = self.format_receive_start(**kwargs)
        LOG.info("cmd:%s", cmd)

        process = my_popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._receive_processes.append(process)
        time.sleep(0.5)

        ret = process.poll()
        if ret is None:
            ret = 0
            error_str = "start netmap receive success"
        else:
            error_str = "start netmap receive failed, %s" % (str(kwargs))
            process.wait()
            self._receive_processes.remove(process)

        return ret, error_str

    def receive_stop(self, **kwargs):
        LOG.info("receive_stop")
        ret = 0
        for process in self._receive_processes:
            process.kill()
            process.wait()
        self._receive_processes = []
        error_str = "stop netmap receive success"
        self._receive_processes = []
        return ret, error_str

    def clean(self):
        self.send_stop()
        self.receive_stop()
        return True

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        kill_by_name('pkt-gen')
        self._send_processes = []
        self._receive_processes = []
        return True


def unit_test():
    perf = Netmap()
    receive = {
        "protocol": "udp_bw",
        # "namespace": "receive",
        "dst": [
            {"iface": "p57p2"}
        ],
    }
    ret = perf.receive_start(**receive)
    LOG.info("*********receive_start***********")
    LOG.info("ret")
    send = {
        # "namespace": "send",
        "protocol": "udp_bw",
        "src": [
            {"iface": "eth4", "mac": "90:e2:ba:20:1f:d8"}
        ],
        "dst": [
            {"mac": "90:e2:ba:20:1f:d9"}
        ],
        "size": 64,
        "threads": 1,
        "ratep": 0
    }
    print perf.send_start(**send)
    print perf._send_processes
    time.sleep(10)

    print perf.send_stop()
    print perf.receive_stop()


if __name__ == "__main__":
    from vstf.common.log import setup_logging

    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf/vstf-netmap.log", clevel=logging.INFO)
    unit_test()
