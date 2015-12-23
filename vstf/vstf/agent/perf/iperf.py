#!/usr/bin/python
# -*- coding: utf8 -*-
# author:
# date: 2015-09-15
# see license for license details

import subprocess
import signal
import os
import time
import logging

import vstf.common.decorator as deco
import vstf.agent.perf.utils as utils
from vstf.common.utils import kill_by_name

LOG = logging.getLogger(__name__)


class Iperf(object):
    def __init__(self):
        self._send_processes = []
        self._receive_processes = []
        self._typemap = {
            "tcp_bw": "",
            "udp_bw": " -u ",
        }

    @deco.check("protocol", choices=['tcp_bw', 'udp_bw'])
    @deco.check("namespace", defaults=None)
    @deco.check("dst")
    @deco.check("time", defaults=600)
    @deco.check("size", defaults=64)
    @deco.check("threads", defaults=1)
    def send_start(self, **kwargs):

        cmd = self.format_send_start(**kwargs)
        LOG.debug("cmd:%s", cmd)

        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        ret = process.poll()
        if ret is None:
            ret = 0
            error_str = "start iperf send success"
            self._send_processes.append(process)
        else:
            print ret
            error_str = "start iperf send failed, %s", (str(kwargs))

        return ret, error_str

    @deco.namespace()
    def format_send_start(self, **kwargs):
        cmd = "iperf %(type)s -c %(dst_ip)s -i 1 -l %(pkt_size)s -t %(time)s  -P %(threads)s "
        context = {
            'type': self._typemap[kwargs['protocol']],
            'dst_ip': kwargs['dst'][0]['ip'],
            'time': kwargs['time'],
            'pkt_size': kwargs['size'],
            'threads': kwargs['threads'],
        }
        cmd = cmd % context
        return cmd

    def send_stop(self):
        results = []
        for process in self._send_processes:
            poll = process.poll()
            if poll is None:
                process.kill()
                ret = 0
                read = "process is stopped by killed"
                results.append((ret, read))

        self._send_processes = []
        return results

    @deco.namespace()
    def format_receive_start(self, **kwargs):
        cmd = 'iperf %s -s ' % (self._typemap[kwargs['protocol']])
        return cmd

    @deco.check("protocol", choices=['tcp_bw', 'udp_bw'])
    @deco.check("namespace", defaults=None)
    def receive_start(self, **kwargs):
        cmd = self.format_receive_start(**kwargs)
        LOG.debug("cmd:%s", cmd)

        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        ret = process.poll()
        if ret is None:
            ret = 0
            error_str = "start iperf receive success"
            self._receive_processes.append(process)
        else:
            print ret
            error_str = "start iperf receive failed, %s" % (str(kwargs))
        return ret, error_str

    def receive_stop(self):
        ret = 0
        for process in self._receive_processes:
            process.kill()
            ret = process.wait()
        self._receive_processes = []
        return ret

    def receive_kill(self):
        ret = 0
        receive_pids = utils.get_pid_by_name('iperf')
        for pid in receive_pids:
            os.kill(pid, signal.SIGKILL)
            time.sleep(0.5)
        error_str = "stop iperf receive success"
        LOG.debug(error_str)
        return ret, error_str

    def force_clean(self):
        LOG.info("%s %s start", self.__class__, self.force_clean.__name__)
        kill_by_name('iperf')
        self._send_processes = []
        self._receive_processes = []
        return True


def unit_test():
    perf = Iperf()
    pro = 'udp_bw'
    print perf.receive_start(namespace='receive', protocol=pro)

    send = {
        "namespace": "send",
        "protocol": "udp_bw",
        "dst": [
            {"ip": "192.168.1.102"}
        ],
        "size": 64,
        "time": 5,
    }
    print perf.send_start(**send)
    time.sleep(10)
    print perf.send_stop()
    print perf.receive_stop()


if __name__ == "__main__":
    from vstf.common.log import setup_logging

    setup_logging(level=logging.DEBUG, log_file="/var/log/vstf-iperf.log", clevel=logging.DEBUG)
    unit_test()
