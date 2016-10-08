##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import shutil
import logging
from vstf.common.utils import check_and_kill, randomMAC, my_mkdir, check_call, check_output, my_sleep
from vstf.agent.env.basic.vm9pfs import VMConfigBy9pfs

LOG = logging.getLogger(__name__)


class VMControlOperation(object):
    """
    a libivrt virsh wrapper for creating virtual machine.
    """

    def __init__(self):
        """
        all tmp files will be created under '/tmp/atf_vm_manager'

        """
        work_dir = '/tmp/atf_vm_manager'
        shutil.rmtree(work_dir, ignore_errors=True)
        my_mkdir(work_dir)
        self.work_dir = work_dir
        self.vnc_index = 0
        self.pci_index = 3
        self.net_index = 0
        self.vm_9p_controllers = {}
        self.vm_configs = {}
        self.image_mgr = None

    @staticmethod
    def composite_xml(context):
        """
        composit a libvirt xml configuration for creating vm from context.

        :param context: a dict containing all necessary options for creating a vm.
        :return: libvirt xml configuration string
        """
        from vm_xml_help import xml_head, xml_disk, xml_ovs, xml_pci, xml_9p, xml_tail, xml_ctrl_br, xml_br
        xml = ''
        tmp = xml_head.replace('VM_NAME', context['vm_name'])
        tmp = tmp.replace('VM_MEMORY', str(context['vm_memory']))
        tmp = tmp.replace('CPU_NUM', str(context['vm_cpu']))
        xml += tmp
        tmp = xml_disk.replace('IMAGE_TYPE', context['image_type'])
        tmp = tmp.replace('IMAGE_PATH', context['image_path'])
        xml += tmp

        if context['9p_path']:
            tmp = xml_9p.replace('9P_PATH', context['9p_path'])
            xml += tmp

        if context['eth_pci']:
            for pci in context['eth_pci']:
                bus = pci[:2]
                slot = pci[3:5]
                func = pci[6:7]
                tmp = xml_pci.replace('BUS', bus)
                tmp = tmp.replace('SLOT', slot)
                tmp = tmp.replace('FUNCTION', func)
                xml += tmp

        if context['ctrl_br']:
            tmp = xml_ctrl_br.replace('CTRL_BR', context['ctrl_br'])
            tmp = tmp.replace('CTRL_MAC', context['ctrl_mac'])
            tmp = tmp.replace('CTRL_MODEL', context['ctrl_model'])
            xml += tmp

        for tap_cfg in context['taps']:
            if tap_cfg['br_type'] == "ovs":
                br_type = "openvswitch"
            else:
                br_type = tap_cfg['br_type']
            if br_type == 'bridge':
                xml_ovs = xml_br
            tmp = xml_ovs.replace('BR_TYPE', br_type)
            tmp = tmp.replace('TAP_MAC', tap_cfg['tap_mac'])
            tmp = tmp.replace('TAP_NAME', tap_cfg['tap_name'])
            tmp = tmp.replace('BR_NAME', tap_cfg['br_name'])
            xml += tmp

        xml += xml_tail
        return xml

    @staticmethod
    def check_required_options(context):
        for key in (
            'vm_name',
            'vm_memory',
            'vm_cpu',
            'image_path',
            'image_type',
                'taps'):
            if key not in context:
                raise Exception("vm config error, must set %s option" % key)

    def set_vm_defaults(self, context):
        vm_9p_path = '%s/%s' % (self.work_dir, context['vm_name'])
        shutil.rmtree(vm_9p_path, ignore_errors=True)
        my_mkdir(vm_9p_path)
        default = {'vm_memory': 4194304,
                   'vm_cpu': 4,
                   'image_type': 'qcow2',
                   'br_type': 'ovs',
                   '9p_path': vm_9p_path,
                   'eth_pci': None,
                   'ctrl_br': 'br0',
                   'ctrl_mac': randomMAC(),
                   'ctrl_model': 'virtio',
                   'ctrl_ip_setting': '192.168.100.100/24',
                   'ctrl_gw': '192.168.100.1'
                   }
        for k, v in default.items():
            context.setdefault(k, v)

    def _shutdown_vm(self):
        out = check_output(
            "virsh list | sed 1,2d | awk '{print $2}'",
            shell=True)
        vm_set = set(out.split())
        for vm in vm_set:
            check_call("virsh shutdown %s" % vm, shell=True)
        timeout = 60
        # wait for gracefully shutdown
        while timeout > 0:
            out = check_output(
                "virsh list | sed 1,2d | awk '{print $2}'",
                shell=True)
            vm_set = set(out.split())
            if len(vm_set) == 0:
                break
            timeout -= 2
            my_sleep(2)
            LOG.info("waiting for vms:%s to shutdown gracefully", vm_set)
        # destroy by force
        for vm in vm_set:
            check_call("virsh destroy %s" % vm, shell=True)
        # undefine all
        out = check_output(
            "virsh list --all | sed 1,2d | awk '{print $2}'",
            shell=True)
        vm_set = set(out.split())
        for vm in vm_set:
            check_call("virsh undefine %s" % vm, shell=True)
        # kill all qemu
        check_and_kill('qemu-system-x86_64')

    def clean_all_vms(self):
        self._shutdown_vm()
        for _, ctrl in self.vm_9p_controllers.items():
            LOG.debug("remove vm9pfs dir:%s", ctrl.vm_9p_path)
            shutil.rmtree(ctrl.vm_9p_path, ignore_errors=True)
        self.vm_9p_controllers = {}
        self.vm_configs = {}
        # shutil.rmtree(self.work_dir, ignore_errors=True)
        self.vnc_index = 0
        self.pci_index = 3
        self.net_index = 0
        self.vms = []
        return True

    def create_vm(self, context):
        self.set_vm_defaults(context)
        self.check_required_options(context)
        xml = self.composite_xml(context)
        vm_name = context['vm_name']
        file_name = os.path.join(self.work_dir, vm_name + '.xml')
        with open(file_name, 'w') as f:
            f.write(xml)
        check_call('virsh define %s' % file_name, shell=True)
        check_call('virsh start %s' % vm_name, shell=True)
        vm_name = context['vm_name']
        vm_9pfs = context['9p_path']
        self.vm_9p_controllers[vm_name] = VMConfigBy9pfs(vm_9pfs)
        self.vm_configs[vm_name] = context
        LOG.debug("%s's vm_9pfs path:%s", vm_name, vm_9pfs)
        return True

    def wait_vm(self, vm_name):
        vm9pctrl = self.vm_9p_controllers[vm_name]
        ret = vm9pctrl.wait_up()
        if ret not in (True,):
            raise Exception(
                'vm running but stuck in boot process, please manully check.')
        LOG.debug('waitVM %s up ok, ret:%s', vm_name, ret)
        return True

    def init_config_vm(self, vm_name):
        """
        using libvirt 9pfs to config boot up options like network ip/gw.

        :param vm_name: the vm to be config with.
        :return: True if succeed, Exception if fail.
        """
        vm_cfg = self.vm_configs[vm_name]
        vm9pctrl = self.vm_9p_controllers[vm_name]
        # print self.vm_9p_controllers
        init_cfg = vm_cfg['init_config']
        if "ctrl_ip_setting" in init_cfg:
            ret = vm9pctrl.config_ip(
                vm_cfg['ctrl_mac'],
                init_cfg['ctrl_ip_setting'])
            assert ret
            LOG.info('initConfigVM config ip ok')
        if 'ctrl_gw' in init_cfg:
            ret = vm9pctrl.config_gw(init_cfg['ctrl_gw'])
            assert ret
            LOG.info('initConfigVM ctrl_gw ok')
        if "ctrl_ip_setting" in init_cfg and "amqp_server" in init_cfg:
            identity = init_cfg['ctrl_ip_setting'].split('/')[0]
            if init_cfg['amqp_id'].strip():
                identity = init_cfg['amqp_id'].strip()
            server = init_cfg['amqp_server']
            port = init_cfg['amqp_port']
            user = init_cfg['amqp_user']
            passwd = init_cfg['amqp_passwd']
            ret = vm9pctrl.config_amqp(identity, server, port, user, passwd)
            assert ret
            LOG.info('initConfigVM config_amqp ok')
        if 'tap_pktloop_config' in init_cfg:
            taps = vm_cfg['taps']
            macs = []
            for tap in taps:
                macs.append(tap['tap_mac'])
            ret = vm9pctrl.set_pktloop_dpdk(macs)
            assert ret
            LOG.info('initConfigVM set_pktloop_dpdk ok')
        return True
