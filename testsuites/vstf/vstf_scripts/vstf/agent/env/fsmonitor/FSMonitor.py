##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import os
import time
import logging
import subprocess
import sys

import constant
from utils import IPCommandHelper, umount, check_and_rmmod, check_output, check_call, call

LOG_FILE = '/tmp/fsmonitor.log'
PID_FILE = '/tmp/fsmonitor.pid'
LOG = logging.getLogger('__name__')


class VMOperation(object):

    def __init__(self):
        self.RTE_SDK = '/home/dpdk-2.0.0'
        self.RTE_TARGET = 'x86_64-native-linuxapp-gcc'
        self.nr_hugepages = '512'
        self.pid = 0
        self.ip_helper = IPCommandHelper()

    def config_ip(self, mac, ip):
        device = self.ip_helper.mac_device_map[mac]
        check_call("ifconfig %s %s up" % (device, ip), shell=True)

    def config_gw(self, ip):
        call("route del default", shell=True)
        check_call("route add default gw %s" % ip, shell=True)

    def recover_nic_binding(self, *tap_macs):
        if self.pid:
            os.kill(self.pid, 9)
            self.pid = None
        bdf_str = ''
        for mac in tap_macs:
            bdf = self.ip_helper.mac_bdf_map[mac]
            bdf_str = bdf_str + ' ' + bdf
        cmd = 'python %s/tools/dpdk_nic_bind.py --bind=virtio-pci %s' % (
            self.RTE_SDK, bdf_str)
        LOG.debug("recover_nic_binding runs cmd = %s", cmd)
        check_call(cmd, shell=True)

    def set_pktloop_dpdk(self, *tap_macs):
        RTE_SDK = self.RTE_SDK
        RTE_TARGET = self.RTE_TARGET
        umount("/mnt/huge")
        with open('/sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages', 'w') as f:
            f.write(self.nr_hugepages)
        check_call("mkdir -p /mnt/huge", shell=True)
        check_call("mount -t hugetlbfs nodev /mnt/huge", shell=True)
        check_call("modprobe uio", shell=True)
        check_and_rmmod('igb_uio')
        check_call(
            "insmod %s/%s/kmod/igb_uio.ko" %
            (RTE_SDK, RTE_TARGET), shell=True)

        bdf_str = ''
        for mac in tap_macs:
            bdf = self.ip_helper.mac_bdf_map[mac]
            bdf_str = bdf_str + ' ' + bdf

        check_call(
            'python %s/tools/dpdk_nic_bind.py --bind=igb_uio %s' %
            (RTE_SDK, bdf_str), shell=True)
        cpu_num = int(
            check_output(
                'cat /proc/cpuinfo | grep processor | wc -l',
                shell=True))
        cpu_bit_mask = 0
        i = cpu_num
        while i:
            cpu_bit_mask = (cpu_bit_mask << 1) + 1
            i -= 1
        cpu_bit_mask = hex(cpu_bit_mask)
        cmd = "%s/%s/app/testpmd -c %s -n %d -- --disable-hw-vlan --disable-rss --nb-cores=%d --rxq=%d --txq=%d --rxd=4096 --txd=4096" % (
            RTE_SDK, RTE_TARGET, cpu_bit_mask, cpu_num / 2, cpu_num - 1, (cpu_num - 1) / 2, (cpu_num - 1) / 2)
        LOG.info("set_pktloop_dpdk runs cmd = %s", cmd)
        p = subprocess.Popen(cmd.split())
        if not p.poll():
            self.pid = p.pid
            return True
        else:
            raise Exception("start testpmd failed")

    def config_amqp(self, file_name):
        if not os.path.isfile(file_name):
            raise Exception("file: %s not exists." % file_name)
        check_call("cp %s /etc/vstf/amqp/amqp.ini" % file_name, shell=True)
        check_call("vstf-agent restart", shell=True)
        return True

    def stop_vstf(self):
        check_call("vstf-agent stop", shell=True)
        return True


class FSMonitor(object):

    def __init__(self, pidfile=None, interval=1):
        if pidfile:
            self.pidfile = pidfile
        else:
            self.pidfile = PID_FILE
        self.interval = interval
        self.handlers = []
        self.kill_old()
        umount(constant.FS_MOUNT_POINT)
        check_call("mkdir -p %s" % constant.FS_MOUNT_POINT, shell=True)
        check_call("mount -t 9p 9pfs %s" % constant.FS_MOUNT_POINT, shell=True)
        os.chdir(constant.FS_MOUNT_POINT)
        with open(constant.VM_UP_Flag_FILE, 'w'):
            pass

    def kill_old(self):
        out = check_output(
            "ps -ef | grep -v grep | egrep 'python.*%s' | awk '{print $2}'" %
            sys.argv[0], shell=True)
        if out:
            for pid in out.split():
                if int(pid) != os.getpid():
                    os.kill(int(pid), 9)
                    LOG.debug("found daemon:pid=%s and kill.", pid)

    def set_fail(self, failed_reason):
        with open(constant.VM_CMD_RETURN_CODE_FILE, 'w') as f:
            f.writelines(
                [constant.VM_CMD_EXCUTE_FAILED_FLAG_CONTENT, '\n', failed_reason])
        with open(constant.VM_CMD_DONE_FLAG_FILE, 'w') as f:
            pass

    def set_success(self):
        with open(constant.VM_CMD_RETURN_CODE_FILE, 'w') as f:
            f.write(constant.VM_CMD_EXCUTE_SUCCES_FLAG_CONTENT)
        with open(constant.VM_CMD_DONE_FLAG_FILE, 'w') as f:
            pass

    def register_handler(self, obj):
        self.handlers.append(obj)

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                'fork #1 failed:%d,(%s)\n' %
                (e.errno, e.strerror))
            sys.exit(1)
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                'fork #2 failed:%d,(%s)\n' %
                (e.errno, e.strerror))
            sys.exit(1)
        LOG.debug(
            "pid:%d,ppid:%d,sid:%d",
            os.getpid(),
            os.getppid(),
            os.getsid(
                os.getpid()))
        old = open('/dev/null', 'r')
        os.dup2(old.fileno(), sys.stdin.fileno())
        old = open('/dev/null', 'a+')
        os.dup2(old.fileno(), sys.stdout.fileno())
        old = open('/dev/null', 'a+', 0)
        os.dup2(old.fileno(), sys.stderr.fileno())
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)

    def run_forever(self):
        # todo:resolve handlers name space conflict
        self.daemonize()
        while True:
            time.sleep(self.interval)
            files = os.listdir(constant.FS_MOUNT_POINT)
            if constant.VM_CMD_SET_FLAG_FILE in files and constant.VM_CMD_CONTENT_FILE in files:
                with open(constant.VM_CMD_CONTENT_FILE, 'r') as f:
                    out = f.read().strip()
                LOG.debug("new command arrived:%s", out)
                cmd_param = out.split()
                cmd = cmd_param[0]
                param = cmd_param[1:]
                for obj in self.handlers:
                    if hasattr(obj, cmd) and callable(getattr(obj, cmd)):
                        LOG.debug("method:%s found!", cmd)
                        method = getattr(obj, cmd)
                        try:
                            method(*param)
                            self.set_success()
                            LOG.debug("cmd sucessfully done")
                        except Exception as e:
                            LOG.debug(
                                'failed to run:%s %s,reason:%s', cmd, param, str(e))
                            self.set_fail(str(e))
                        break
                else:
                    LOG.debug("method:%s not found!", cmd)
                    self.set_fail(constant.VM_CMD_NOT_FOUND)
                os.remove(constant.VM_CMD_SET_FLAG_FILE)
                os.remove(constant.VM_CMD_CONTENT_FILE)


if __name__ == '__main__':
    # echo "set_pktloop_dpdk" > command;touch command_set
    # echo "recover_nic_binding" > command;touch command_set
    # echo "config_ip 56:6f:44:a5:3f:a2 192.168.188.200/23" > command;touch command_set
    # echo "config_gw 192.168.188.1" > command;touch command_set
    # echo set_pktloop_dpdk 56:6f:44:a5:3f:a2 56:6f:44:a5:3f:a3 > command;touch command_set
    # echo recover_nic_binding 56:6f:44:a5:3f:a2 56:6f:44:a5:3f:a3 >
    # command;touch command_set
    import os
    logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode='w')
    os.environ['PATH'] = os.environ["PATH"] + ":/usr/local/bin"
    LOG.info(os.environ['PATH'])
    vm_op = VMOperation()
    agent = FSMonitor()
    agent.register_handler(vm_op)
    agent.run_forever()
