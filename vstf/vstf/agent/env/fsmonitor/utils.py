"""
Created on 2015-7-8

@author: y00228926
"""
import subprocess
from StringIO import StringIO
import re
import logging

LOG = logging.getLogger(__name__)


def call(cmd, shell=False):
    if shell:
        LOG.info(cmd)
    else:
        LOG.info(' '.join(cmd))
    return subprocess.call(cmd, shell=shell)


def check_call(cmd, shell=False):
    if shell:
        LOG.info(cmd)
    else:
        LOG.info(' '.join(cmd))
    subprocess.check_call(cmd, shell=shell)


def check_output(cmd, shell=False):
    if shell:
        LOG.info(cmd)
    else:
        LOG.info(' '.join(cmd))
    return subprocess.check_output(cmd, shell=shell)


def check_and_kill(process):
    cmd = "ps -ef | grep -v grep | awk '{print $8}' | grep -w %s | wc -l" % process
    out = check_output(cmd, shell=True)
    if int(out):
        check_call(['killall', process])


def check_and_rmmod(mod):
    cmd = "lsmod | awk '{print $1}' | grep -w %s | wc -l" % mod
    out = check_output(cmd, shell=True)
    if int(out):
        check_call(['rmmod', mod])


def umount(path):
    mount_path_set = set()
    out = check_output("cat /proc/mounts", shell=True)
    f = StringIO(out)
    line = f.readline()
    while line:
        line = f.readline()
        if line:
            mpath = line.split()[1]
            mount_path_set.add(mpath)
    if path in mount_path_set:
        ret = call("umount %s" % path, shell=True)
        return ret == 0
    return True


class IPCommandHelper(object):
    def __init__(self):
        self.devices = []
        self.macs = []
        self.device_mac_map = {}
        self.mac_device_map = {}
        self.bdf_device_map = {}
        self.device_bdf_map = {}
        self.mac_bdf_map = {}
        self.bdf_mac_map = {}
        buf = check_output("ip link", shell=True)
        macs = re.compile("[A-F0-9]{2}(?::[A-F0-9]{2}){5}", re.IGNORECASE | re.MULTILINE)
        for mac in macs.findall(buf):
            if mac.lower() in ('00:00:00:00:00:00', 'ff:ff:ff:ff:ff:ff'):
                continue
            self.macs.append(mac)
        sio = StringIO(buf)
        for line in sio:
            m = re.match(r'^\d+:(.*):.*', line)
            if m and m.group(1).strip() != 'lo':
                self.devices.append(m.group(1).strip())
        for device, mac in zip(self.devices, self.macs):
            self.device_mac_map[device] = mac
            self.mac_device_map[mac] = device
        for device in self.devices:
            buf = check_output("ethtool -i %s" % device, shell=True)
            bdfs = re.findall(r'^bus-info: \d{4}:(\d{2}:\d{2}\.\d*)$', buf, re.MULTILINE)
            if bdfs:
                self.bdf_device_map[bdfs[0]] = device
                self.device_bdf_map[device] = bdfs[0]
                mac = self.device_mac_map[device]
                self.mac_bdf_map[mac] = bdfs[0]
                self.bdf_mac_map[bdfs[0]] = mac


if __name__ == '__main__':
    ip_helper = IPCommandHelper()
    print ip_helper.device_mac_map
    print ip_helper.mac_device_map
    print ip_helper.bdf_device_map
    print ip_helper.device_bdf_map
    print ip_helper.mac_bdf_map
    print ip_helper.bdf_mac_map
