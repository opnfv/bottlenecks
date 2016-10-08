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
import vstf.common.decorator as deco
from vstf.common import perfmark as mark
from vstf.common.utils import kill_by_name, my_popen

LOG = logging.getLogger(__name__)


class Qperf(object):

    def __init__(self):
        self._send_processes = []
        self._receive_processes = []

    @deco.check("protocol", choices=['tcp_lat', 'udp_lat'])
    @deco.check("namespace", defaults=None)
    @deco.check("dst")
    @deco.check("time", defaults=10)
    @deco.check("size", defaults=64)
    def send_start(self, **kwargs):
        cmd = self.format_send_start(**kwargs)
        LOG.info("cmd:%s", cmd)
        process = my_popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        time.sleep(0.5)
        ret = process.poll()
        if ret is None:
            ret = 0
            error_str = "start qperf send success"
            self._send_processes.append(process)
        else:
            print ret
            error_str = "start qperf send failed, %s" % (str(kwargs))
            process.wait()

        return ret, error_str

    @deco.namespace()
    def format_send_start(self, **kwargs):
        cmd = "qperf %(dst_ip)s -t %(time)s -m %(pkt_size)s -vu %(type)s "
        context = {
            'dst_ip': kwargs['dst'][0]['ip'],
            'type': kwargs['protocol'],
            'time': kwargs['time'],
            'pkt_size': kwargs['size'],
        }
        cmd = cmd % context
        return cmd

    def send_stop(self, **kwargs):
        results = []
        for process in self._send_processes:
            process.wait()
            read = process.stdout.read()
            read = self._parse_data(read)
            ret = 0
            results.append((ret, read))
        self._send_processes = []
        return results

    @deco.namespace()
    def format_receive_start(self, **kwargs):
        cmd = 'qperf'
        return cmd

    def receive_start(self, **kwargs):
        cmd = self.format_receive_start(**kwargs)
        LOG.info("cmd:%s", cmd)

        process = my_popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        time.sleep(0.5)
        ret = process.poll()
        if ret is None:
            ret = 0
            error_str = "start qperf receive success"
            self._receive_processes.append(process)
        else:
            print ret
            error_str = "start qperf receive failed, %s" % (str(kwargs))
            process.wait()
            raise Exception(error_str)
        return ret, error_str

    def receive_stop(self, **kwargs):
        ret = 0
        for process in self._receive_processes:
            process.kill()
            process.wait()
        self._receive_processes = []
        error_str = "stop qperf receive success"
        return ret, error_str

    def receive_kill(self):
        kill_by_name('qperf')
        self._receive_processes = []
        return True

    def clean(self):
        for process in self._receive_processes:
            process.kill()
            process.wait()
            LOG.info("process.kill(qperf daemon:%s)", process.pid)
        for process in self._send_processes:
            LOG.info("process.wait(qperf client:%s)", process.pid)
            process.wait()
        self._receive_processes = []
        self._send_processes = []
        return True

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        kill_by_name('qperf')
        self._send_processes = []
        self._receive_processes = []
        return True

    def _parse_data(self, data):
        LOG.info(data)
        latency = 0
        if data:
            buf = data.splitlines()
            if "latency" in buf[1]:
                data = buf[1].strip().split()
                if data[3] == "us":
                    latency = float(data[2]) / 1000
                else:
                    latency = float(data[2])
        result = {
            mark.minLatency: latency,
            mark.avgLatency: latency,
            mark.maxLatency: latency
        }
        return result


def unit_test():
    perf = Qperf()
    perf.receive_start(namespace='receive')

    send = {
        "namespace": "send",
        "protocol": "udp_lat",
        "dst": [
            {"ip": "192.168.1.102"}
        ],
        "size": 64,
    }
    print perf.send_start(**send)
    time.sleep(10)
    print perf.send_stop()
    print perf.receive_stop()


if __name__ == "__main__":
    from vstf.common.log import setup_logging

    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-qperf.log",
        clevel=logging.DEBUG)
    unit_test()
