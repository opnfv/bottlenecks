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
import vstf.common.constants as cst
import vstf.common.decorator as deco
from vstf.common import perfmark as mark
from vstf.common.utils import kill_by_name, my_popen

import logging

LOG = logging.getLogger(__name__)


class Netperf(object):

    def __init__(self):
        self._send_processes = []
        self._islat = False
        self._typemap = {
            "tcp_lat": "TCP_STREAM",
            "tcp_bw": "TCP_STREAM",
            "udp_lat": "UDP_STREAM",
            "udp_bw": "UDP_STREAM",
        }

    @deco.check("protocol", choices=cst.PROTOCOLS)
    @deco.check("namespace", defaults=None)
    @deco.check("dst")
    @deco.check("time", defaults=0)
    @deco.check("size", defaults=64)
    @deco.check("threads", defaults=1)
    def send_start(self, **kwargs):
        threads = kwargs.pop('threads')
        kwargs['buf'] = cst.SOCKET_BUF
        if kwargs['protocol'] in ['tcp_lat', 'udp_lat']:
            self._islat = True
        else:
            kwargs['time'] = 0

        cmd = self.format_send_start(**kwargs)
        LOG.info("cmd:%s", cmd)

        for _ in range(threads):
            process = my_popen(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            self._send_processes.append(process)
        time.sleep(0.5)
        for process in self._send_processes:
            ret = process.poll()
            if ret is None:
                ret = 0
                error_str = "start netperf send success"
            else:
                error_str = "start netperf send failed, %s" % (str(kwargs))
                process.wait()
                self._send_processes.remove(process)

        return ret, error_str

    def send_stop(self, **kwargs):
        LOG.info("send_stop")
        results = []
        ret = 0
        for process in self._send_processes:
            poll = process.poll()
            if poll is None:
                if not self._islat:
                    process.kill()
                    read = "process is stopped by killed"
                else:
                    ret = process.wait()
                    read = process.stdout.read()
                    read = self._parse_data(read)
                results.append((ret, read))
        self._send_processes = []
        self._islat = False
        return results

    @staticmethod
    def _parse_data(data):
        buf = data.splitlines()
        data = buf[2].strip().split(',')
        result = {
            mark.minLatency: float(data[0]),
            mark.avgLatency: float(data[1]),
            mark.maxLatency: float(data[2])
        }
        return result

    @deco.namespace()
    def format_send_start(self, **kwargs):
        #       cmd = "netperf -H %(dst_ip)s -t %(type)s -l %(time)s -- -m %(pkt_size)s "
        cmd = "netperf -H %(dst_ip)s -t %(type)s -l %(time)s  " \
              "-- -m %(pkt_size)s -s %(buf)s -S %(buf)s -o  MIN_LATENCY,MEAN_LATENCY,MAX_LATENCY"
        context = {
            'dst_ip': kwargs['dst'][0]['ip'],
            'type': self._typemap[kwargs['protocol']],
            'time': kwargs['time'],
            'pkt_size': kwargs['size'],
            'buf': kwargs['buf'],
        }
        cmd = cmd % context
        return cmd

    @deco.namespace()
    def format_receive_start(self, **kwargs):
        cmd = 'netserver'
        return cmd

    @deco.check("namespace")
    def receive_start(self, **kwargs):

        cmd = self.format_receive_start(**kwargs)
        LOG.info("cmd:%s", cmd)

        process = my_popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        time.sleep(0.5)
        ret = process.poll()
        if ret:
            error_str = "start netserver failed, %s" % (str(kwargs))
        else:
            ret = 0
            error_str = "start netserver success"

        return ret, error_str

    def receive_stop(self, **kwargs):
        LOG.info("receive_stop")
        ret = 0
        kill_by_name('netserver')
        time.sleep(0.5)
        error_str = "stop netserver success"
        return ret, error_str

    def clean(self):
        self.send_stop()
        self.receive_stop()
        return True

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        kill_by_name('netserver')
        kill_by_name('netperf')
        self._send_processes = []
        self._receive_processes = []
        return True


def unit_test():
    perf = Netperf()
    ret = perf.receive_start(namespace='receive')
    print "*********receive_start***********"
    print ret
    send = {
        "namespace": "send",
        "protocol": "udp_lat",
        "dst": [
            {"ip": "192.168.1.102"}
        ],
        "size": 64,
        "threads": 1,
        "time": 10,
    }
    print perf.send_start(**send)
    print perf._send_processes
    time.sleep(10)
    print perf.send_stop()
    print perf.receive_stop()


if __name__ == "__main__":
    from vstf.common.log import setup_logging

    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-netperf.log",
        clevel=logging.DEBUG)
    unit_test()
