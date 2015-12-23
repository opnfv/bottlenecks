import re
import logging
import subprocess
import random
import os
import signal
import time
from StringIO import StringIO

LOG = logging.getLogger(__name__)


def info():
    def _deco(func):
        def __deco(*args, **kwargs):
            if "shell" in kwargs and not kwargs["shell"]:
                LOG.info(' '.join(args[0]))
            else:
                LOG.info(args[0])
            return func(*args, **kwargs)
        return __deco
    return _deco


@info()
def call(cmd, shell=False):
    ret = subprocess.call(cmd, shell=shell)
    if ret != 0:
        LOG.info("warning: %s not success.", cmd)


@info()
def check_call(cmd, shell=False):
    subprocess.check_call(cmd, shell=shell)


@info()
def check_output(cmd, shell=False):
    return subprocess.check_output(cmd, shell=shell)


@info()
def my_popen(cmd, shell=False, stdout=None, stderr=None):
    return subprocess.Popen(cmd, shell=shell, stdout=stdout, stderr=stderr)


def ping(ip):
    cmd = "ping -w2 -c1 %s" % ip
    p = my_popen(cmd, shell=True)
    return 0 == p.wait()


def get_device_name(bdf):
    path = '/sys/bus/pci/devices/0000:%s/net/' % bdf
    path1 = '/sys/bus/pci/devices/0000:%s/virtio*/net/' % bdf
    if os.path.exists(path):
        device = check_output("ls " + path, shell=True).strip()
        return device
    else:  # virtio driver
        try:
            device = check_output("ls " + path1, shell=True).strip()
            return device
        except Exception:
            return None


def my_sleep(delay):
    LOG.info('sleep %s' % delay)
    time.sleep(delay)


def my_mkdir(filepath):
    try:
        LOG.info("mkdir -p %s" % filepath)
        os.makedirs(filepath)
    except OSError, e:
        if e.errno == 17:
            LOG.info("! %s already exists" % filepath)
        else:
            raise


def get_eth_by_bdf(bdf):
    bdf = bdf.replace(' ', '')
    path = '/sys/bus/pci/devices/0000:%s/net/' % bdf
    if os.path.exists(path):
        device = check_output("ls " + path, shell=True).strip()
    else:
        raise Exception("cann't get device name of bdf:%s" % bdf)
    return device


def check_and_kill(process):
    cmd = "ps -ef | grep -v grep | awk '{print $8}' | grep -w %s | wc -l" % process
    out = check_output(cmd, shell=True)
    if int(out):
        check_call(['killall', process])


def list_mods():
    return check_output("lsmod | sed 1,1d | awk '{print $1}'", shell=True).split()


def check_and_rmmod(mod):
    if mod in list_mods():
        check_call(['rmmod', mod])


def kill_by_name(process):
    out = check_output(['ps', '-A'])
    for line in out.splitlines():
        values = line.split()
        pid, name = values[0], values[3]
        if process == name:
            pid = int(pid)
            os.kill(pid, signal.SIGKILL)
            LOG.info("os.kill(%s)" % pid)


def ns_cmd(ns, cmd):
    netns_exec_str = "ip netns exec %s "
    if ns in (None, 'null', 'None', 'none'):
        pass
    else:
        cmd = (netns_exec_str % ns) + cmd
    return cmd


def randomMAC():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


class IPCommandHelper(object):
    def __init__(self, ns=None):
        self.devices = []
        self.macs = []
        self.device_mac_map = {}
        self.mac_device_map = {}
        self.bdf_device_map = {}
        self.device_bdf_map = {}
        self.mac_bdf_map = {}
        self.bdf_mac_map = {}
        cmd = "ip link"
        if ns:
            cmd = "ip netns exec %s " % ns + cmd
        buf = check_output(cmd, shell=True)
        sio = StringIO(buf)
        for line in sio:
            m = re.match(r'^\d+:(.*):.*', line)
            if m and m.group(1).strip() != "lo":
                device = m.group(1).strip()
                self.devices.append(device)
                mac = self._get_mac(ns, device)
                self.macs.append(mac)
        for device, mac in zip(self.devices, self.macs):
            self.device_mac_map[device] = mac
            self.mac_device_map[mac] = device

        cmd = "ethtool -i %s"
        if ns:
            cmd = "ip netns exec %s " % ns + cmd
        for device in self.devices:
            buf = check_output(cmd % device, shell=True)
            bdfs = re.findall(r'^bus-info: \d{4}:(\d{2}:\d{2}\.\d*)$', buf, re.MULTILINE)
            if bdfs:
                self.bdf_device_map[bdfs[0]] = device
                self.device_bdf_map[device] = bdfs[0]
                mac = self.device_mac_map[device]
                self.mac_bdf_map[mac] = bdfs[0]
                self.bdf_mac_map[bdfs[0]] = mac

    @staticmethod
    def _get_mac(ns, device):
        cmd = "ip addr show dev %s" % device
        if ns:
            cmd = "ip netns exec %s " % ns + cmd
        buf = check_output(cmd, shell=True)
        macs = re.compile(r"[A-F0-9]{2}(?::[A-F0-9]{2}){5}", re.IGNORECASE | re.MULTILINE)
        for mac in macs.findall(buf):
            if mac.lower() not in ('00:00:00:00:00:00', 'ff:ff:ff:ff:ff:ff'):
                return mac
        return None

    def get_device_verbose(self, identity):
        if identity in self.device_mac_map:
            device = identity
        elif identity in self.bdf_device_map:
            device = self.bdf_device_map[identity]
        elif identity in self.mac_device_map:
            device = self.mac_device_map[identity]
        else:
            raise Exception("cann't find the device by identity:%s" % identity)
        detail = {
            'bdf': self.device_bdf_map[device] if device in self.device_bdf_map else None,
            'iface': device,
            'mac': self.device_mac_map[device] if device in self.device_mac_map else None,
        }
        return detail


class AttrDict(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.  """

    def __init__(self, init={}):
        dict.__init__(self, init)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(AttrDict, self).__getitem__(name)

    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = AttrDict(self)
        return ch


if __name__ == "__main__":
    ipcmd = IPCommandHelper()
    print ipcmd.device_mac_map
    print ipcmd.mac_device_map
    print ipcmd.bdf_device_map
    print ipcmd.device_bdf_map
    print ipcmd.mac_bdf_map
    print ipcmd.bdf_mac_map
    print ipcmd.get_device_verbose("tap0")
