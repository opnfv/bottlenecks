##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import logging
import textwrap
from vstf.common.utils import my_sleep
from vstf.agent.env.fsmonitor import constant

LOG = logging.getLogger(__name__)


class VMConfigBy9pfs(object):
    """
    host side implemetation of a self-defined communication protocol using libvirt 9pfs to give commands to the Virtual Machine.

    """

    def __init__(self, vm_9p_path):
        """
        :param vm_9p_path: The host path of libvirt 9pfs for a vm.
        :return:
        """
        self.vm_9p_path = vm_9p_path

    def clean(self):
        self._unlink(self._path(constant.VM_CMD_RETURN_CODE_FILE))
        self._unlink(self._path(constant.VM_CMD_DONE_FLAG_FILE))

    def _path(self, relative_path):
        return os.path.join(self.vm_9p_path, relative_path)

    def _unlink(self, file_path):
        os.unlink(file_path)
        LOG.info("os.unlink(%s)", file_path)

    def _read(self, filename):
        filepath = self._path(filename)
        with open(filepath, 'r') as f:
            ret = f.read()
            LOG.info("read(%s) -> %s", filepath, ret)
        return ret

    def _write(self, filename, cmd):
        filepath = self._path(filename)
        with open(filepath, 'w') as f:
            f.write("%s" % cmd)
            LOG.info("write(%s) <- %s", filepath, cmd)

    def _wait_flag_file_to_exist(self, filename, timeout):
        filepath = self._path(filename)
        while timeout > 0:
            if os.path.exists(filepath):
                LOG.info("wait and find file:%s", filepath)
                return True
            my_sleep(1)
            timeout -= 1
            LOG.info("waiting file to exist:%s", filepath)
        return False

    def _get_cmd_return_code(self):
        ret = self._read(constant.VM_CMD_RETURN_CODE_FILE)
        return ret == constant.VM_CMD_EXCUTE_SUCCES_FLAG_CONTENT

    def _wait_command_done(self):
        done = self._wait_flag_file_to_exist(
            constant.VM_CMD_DONE_FLAG_FILE,
            constant.VM_COMMON_CMD_EXCUTE_TIME_OUT)
        if done:
            return self._get_cmd_return_code()
        else:
            return 'timeout'

    def _set_cmd(self, cmd):
        self._write(constant.VM_CMD_CONTENT_FILE, cmd)
        self._write(constant.VM_CMD_SET_FLAG_FILE, '')
        ret = self._wait_command_done()
        if ret:
            self.clean()
            return ret
        else:
            raise Exception("9pfs command failure: timeout.")

    def wait_up(self):
        return self._wait_flag_file_to_exist(
            constant.VM_UP_Flag_FILE, constant.VM_UP_TIME_OUT)

    def config_ip(self, mac, ip):
        cmd = 'config_ip %s %s' % (mac, ip)
        return self._set_cmd(cmd)

    def config_gw(self, ip):
        cmd = 'config_gw %s' % ip
        return self._set_cmd(cmd)

    def set_pktloop_dpdk(self, macs):
        """
        To connect two network devices together in the vm and loop the packets received to another.
        Use dpdk testpmd to loop the packets. See FSMonitor.

        :param macs: the mac address list of network cards of the vm.
        :return: True for success, Exception for Failure.
        """
        mac_str = ' '.join(macs)
        cmd = 'set_pktloop_dpdk ' + mac_str
        return self._set_cmd(cmd)

    def recover_nic_binding(self, macs):
        """
        in contrast to set_pktloop_dpdk, disconnect the looping.
        :param macs:  the mac address list of network cards of the vm.
        :return: True for success, Exception for Failure.
        """
        mac_str = ' '.join(macs)
        cmd = 'recover_nic_binding ' + mac_str
        return self._set_cmd(cmd)

    def config_amqp(
            self,
            identity,
            server,
            port=5672,
            user="guest",
            passwd="guest"):
        data = {
            'server': server,
            'port': port,
            'id': identity,
            'user': user,
            'passwd': passwd
        }
        header = "[rabbit]"
        content = '''
        user=%(user)s
        passwd=%(passwd)s
        host=%(server)s
        port=%(port)s
        id=%(id)s''' % data
        file_name = "amqp.ini"
        dedented_text = textwrap.dedent(content)
        self._write(file_name, header + dedented_text)
        cmd = 'config_amqp %s' % file_name
        return self._set_cmd(cmd)

    def stop_vstf(self):
        cmd = "stop_vstf"
        return self._set_cmd(cmd)

    def __repr__(self):
        return self.__class__.__name__ + ':' + self.vm_9p_path


if __name__ == '__main__':
    fs = VMConfigBy9pfs('/tmp/tmp4T6p7L')
    print os.listdir(os.curdir)
    print fs.config_ip('56:6f:44:a5:3f:a4', '192.168.188.200/23')
    print fs.config_gw('192.168.188.1')
    print fs.set_pktloop_dpdk(['56:6f:44:a5:3f:a2', '56:6f:44:a5:3f:a3'])
    print fs.recover_nic_binding(['56:6f:44:a5:3f:a2', '56:6f:44:a5:3f:a3'])
    print fs.config_amqp('192.168.188.200', '192.168.188.10')
    print os.listdir(os.curdir)
