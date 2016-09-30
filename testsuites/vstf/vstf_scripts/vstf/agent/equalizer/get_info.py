##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import commands

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class GetPhyInfo(object):

    def __init__(self):
        pass

    def _get_range(self, temp):
        topo = {}
        phy_core_flag = True
        for sub in temp.split(','):
            r_list = []
            _start = sub.split('-')[0]
            _end = sub.split('-')[1]
            r_list.extend(range(int(_start), int(_end) + 1))
            if phy_core_flag:
                topo['phy_cores'] = r_list
            else:
                topo['virt_cores'] = r_list
            phy_core_flag = False
        return topo

    def _get_numa_num(self):
        flag, num = commands.getstatusoutput('lscpu | grep "NUMA node(s):"')
        try:
            num = num.split(':')[1]
        except:
            print('get numa %s value failed.' % (num))
        return num

    def get_numa_core(self):
        numa = {}
        num = self._get_numa_num()
        for numa_id in range(0, int(num)):
            flag, temp = commands.getstatusoutput(
                'lscpu | grep "NUMA node%s"' %
                (str(numa_id)))
            try:
                temp = temp.split(':')[1].split()[0]
            except:
                print('get numa %s range %s failed.' % (str(numa_id), range))
            topo = self._get_range(temp)
            numa['node' + str(numa_id)] = topo
        return str(numa)

    def get_nic_numa(self, nic):
        result = {}
        try:
            flag, id = commands.getstatusoutput(
                'cat /sys/class/net/%s/device/numa_node' %
                (nic))
        except:
            print('get nic numa id failed.')
        return id

    def _get_main_pid(self, xml_file):
        try:
            tree = ET.ElementTree(file=xml_file)
            root = tree.getroot()
            _main_pid = root.attrib['pid']
        except:
            print('[ERROR]Parse xml file failed, could not get qemu main pid')
        return _main_pid

    def _get_qemu_threads(self, xml_file):
        # import pdb
        # pdb.set_trace()
        _qemu_threads = []
        try:
            tree = ET.ElementTree(file=xml_file)
            root = tree.getroot()
            for element in tree.iterfind('vcpus/vcpu'):
                _qemu_threads.append(element.attrib['pid'])
        except:
            print('[ERROR]Parse xml file failed, could not get qemu threads.')

        return _qemu_threads

    def _get_mem_numa(self, xml_file):
        try:
            _mem_numa = None
            tree = ET.ElementTree(file=xml_file)
            root = tree.getroot()
            for element in tree.iterfind('domain/numatune/memory'):
                _mem_numa = element.attrib['nodeset']
        finally:
            return _mem_numa

    def _get_vhost_threads(self, xml_file):
        _vhost = []
        _main_pid = self._get_main_pid(xml_file)

        # get vhost info
        proc_name = 'vhost-' + _main_pid
        flag, temp = commands.getstatusoutput(
            'ps -ef | grep %s | grep -v grep' %
            (proc_name))
        for line in temp.split('\n'):
            try:
                vhost = line.split()[1]
                _vhost.append(vhost)
            except:
                print('get vhost %s proc id failed' % (line))

        return _vhost

    def get_vm_info(self, vm_name):
        vm = {}
        src_path = '/var/run/libvirt/qemu/'
        xml_file = src_path + vm_name + '.xml'

        # get vm main pid from file
        _main_pid = self._get_main_pid(xml_file)
        # get vm vcpu thread from the libvirt file
        _qemu_threads = self._get_qemu_threads(xml_file)
        # get vm bind mem numa id
        _mem_numa = self._get_mem_numa(xml_file)
        # get vhost thread
        _vhosts = self._get_vhost_threads(xml_file)

        vm['main_pid'] = _main_pid
        vm['qemu_thread'] = _qemu_threads
        vm['mem_numa'] = _mem_numa
        vm['vhost_thread'] = _vhosts
        return vm

    def _get_proc_by_irq(self, irq):
        try:
            flag, info = commands.getstatusoutput(
                'ps -ef | grep irq/%s | grep -v grep ' % (irq))
            proc_id = info.split('\n')[0].split()[1]
        except:
            print("[ERROR]grep process id failed.")
        return proc_id

    def get_nic_interrupt_proc(self, nic):
        _phy_nic_thread = []
        flag, info = commands.getstatusoutput(
            'cat /proc/interrupts | grep %s' % (nic))
        for line in info.split('\n'):
            try:
                irq_num = line.split(':')[0].split()[0]
                proc_id = self._get_proc_by_irq(irq_num)
                _phy_nic_thread.append([irq_num, proc_id])
            except:
                print("[ERROR]get irq num failed.")
        return _phy_nic_thread

    def get_libvirt_vms(self):
        vm_list = []
        flag, info = commands.getstatusoutput('virsh list')
        list = info.split('\n')
        if list[-1] == '':
            list.pop()
        del list[0]
        del list[0]

        for line in list:
            try:
                vm_temp = line.split()[1]
                vm_list.append(vm_temp)
            except:
                print("Get vm name failed from %s" % (line))
        return vm_list
