##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import re
import copy
import time
import ConfigParser

fwd = {'single': ['forward'],
       'double': ['forward', 'reverse']
       }
models = ['Tnv']
direction = ['single', 'double']
reverse_dict = {
    'forward': 'reverse',
    'reverse': 'forward'
}


class BaseModel(object):

    def __init__(self, config):
        self.config = config

    def _check_model(self):
        return self.config['model'] in models

    def _check_virtenv(self):
        try:
            num = int(self.config['virtenv'])
            return num in range(1, 9)
        except:
            print("[ERROR]The virtenv is not a inter number.")

    def _check_queues(self):
        try:
            num = int(self.config['queues'])
            return num in range(1, 9)
        except:
            print("[ERROR]The virt queues is not a inter number.")

    @property
    def _check_flows(self):
        try:
            num = int(self.config['flows'])
            return num in range(1, 9)
        except:
            print("[ERROR]The flow is not a inter number.")

    def _check_direct(self):
        return self.config['direct'] in direction

    def _check_vlans(self):
        return self.config['vlans'] in ['True', 'False']

    def _check_bind(self):
        return True

    def check_parameter_invalid(self):
        try:
            if self._check_model() and \
                    self._check_virtenv() and \
                    self._check_queues() and \
                    self._check_flows and \
                    self._check_direct() and \
                    self._check_vlans() and \
                    self._check_bind():
                return True
            else:
                print("[ERROR]Paramter check invalid")
                return False
        except:
            print("[ERROR]Check parameter invalid with unknown reason.")
            return False


def _get_array_values(irq_array):
    proc_list = []
    for i in range(len(irq_array)):
        proc_list.append(irq_array[i][1])
    return sorted(proc_list)


def check_dict(thread_info, flow):
    if thread_info['src_recv_irq'] != flow['src_recv_irq']:
        print("[WARN]Flow src_irq process %s not match %s in the table."
              % (thread_info['src_recv_irq'],
                 flow['src_recv_irq']))
        return False
    if thread_info['dst_send_irq'] != flow['dst_send_irq']:
        print("[WARN]Flow dst_irq process %s not match %s in the table."
              % (thread_info['dst_send_irq'],
                 flow['dst_send_irq']))
        return False
    return True


def dst_ip_update(flow):
    try:
        src_dst_ip = flow['dst_ip']
        ip_section = '.'.join(src_dst_ip.split('.')[0:3]) + '.'
        number = int(src_dst_ip.split('.')[3])
        new_number = number + 1
        new_dst_ip = ip_section + str(new_number)
        flow['dst_ip'] = new_dst_ip
    except:
        print("[ERROR]dst ip update failed.")


def _tranfer_array_to_range(array):
    return str(array[0]) + '-' + str(array[-1])


class TnV(BaseModel):

    def __init__(self, config):
        super(TnV, self).__init__(config)
        self.config = config
        self.host_instance = None
        self.send_instace = None
        self.vms = None
        self.init_flows = {}
        handle = ConfigParser.ConfigParser()
        handle.read(self.config['configfile'])
        self.handle = handle

    def _get_vms(self):
        return self.host_instance.get_libvirt_vms()

    def flow_match(self):
        _queues = int(self.config['queues'])
        _virtenv = int(self.config['virtenv'])
        _flows = int(self.config['flows'])
        return _flows == _queues * _virtenv

    def match_virt_env(self):
        try:
            self.vms = self._get_vms()
            return len(self.vms) == int(self.config['virtenv'])
        except:
            print("[ERROR]vms or containers number is equal to virtenv.")
            return False

    @property
    def match_flows_and_nic(self):
        # get src_nic
        for section in ['send', 'recv']:
            nic = self._get_nic_from_file(section, 'nic')
            try:
                irq_proc = self.host_instance.get_nic_interrupt_proc(nic)
                return int(self.config['flows']) == len(irq_proc)
            except:
                print("[ERROR]match flow with nic interrupt failed.")
                return False

    def _get_nic_irq_proc(self, nic):
        return self.host_instance.get_nic_interrupt_proc(nic)

    def _get_nic_from_file(self, section, column):
        return self.handle.get(section, column)

    def _get_range(self, section, column):
        try:
            info = self.handle.get(section, column)
            return info.split(' ')
        except:
            print("[ERROR]Get mac failed.")
            return False

    def check_mac_valid(self):
        flag = True
        try:
            for option in ['send', 'recv']:
                info = self.handle.get(option, 'macs')
                macs = info.split()
                if len(macs) != int(self.config['virtenv']) or macs == []:
                    print(
                        "[ERROR]The macs number is not equal to vms or containers.")
                    return False
                for mac in macs:
                    # check mac valid
                    if re.match(r'..:..:..:..:..:..', mac):
                        continue
                    else:
                        print("[ERROR]mac %s invalid" % mac)
                        flag = False
                        break
                if not flag:
                    break
            return flag
        except:
            print("[ERROR]parse macs failed.")
            return False

    def check_vlan_valid(self):
        flag = True
        for direct in ['send', 'recv']:
            vlans = self.handle.get(direct, 'vlans').split()
            if len(vlans) != int(self.config['virtenv']):
                print("[ERROR]vlan un config")
                return False
            for vlan in vlans:
                if int(vlan) <= 1 or int(vlan) >= 4095:
                    flag = False
                    break
        return flag

    @property
    def check_logic_invalid(self):
        return self.flow_match() and self.match_virt_env() and \
            self.match_flows_and_nic and self.check_mac_valid() and \
            self.check_vlan_valid()

    @property
    def read_flow_init(self):
        # The
        temp_flow = {}
        src_macs = self._get_range('send', 'macs')
        dst_macs = self._get_range('recv', 'macs')
        src_vlan = self._get_range('send', 'vlans')
        dst_vlan = self._get_range('recv', 'vlans')
        src_nic = self._get_nic_from_file('send', 'nic')
        dst_nic = self._get_nic_from_file('recv', 'nic')
        src_nic_irq = _get_array_values(self._get_nic_irq_proc(src_nic))
        dst_nic_irq = _get_array_values(self._get_nic_irq_proc(dst_nic))
        src_ip_sections = self._get_range('send', 'ip_sections')
        dst_ip_sections = self._get_range('recv', 'ip_sections')
        send_port = self._get_nic_from_file('send', 'port')
        recv_port = self._get_nic_from_file('recv', 'port')
        temp_flow['tester_ip'] = self._get_nic_from_file('common', 'tester_ip')
        vlan = src_vlan
        avg_flow = int(self.config['flows']) / int(self.config['virtenv'])
        # build the main dictionary
        for _direct in sorted(fwd[self.config['direct']]):
            i = 0
            j = 0
            temp_flow['direct'] = _direct
            temp_flow['send_port'] = send_port
            temp_flow['recv_port'] = recv_port

            for _vm in sorted(self.vms):
                vlan_id = {
                    'True': vlan[i],
                    'False': None}
                temp_flow['virt'] = _vm
                _vm_info = self.host_instance.get_vm_info(_vm)
                temp_flow['qemu_proc'] = _vm_info['main_pid']
                # temp_flow['qemu_thread']  = _vm_info['qemu_thread']
                temp_flow['mem_numa'] = _vm_info['mem_numa']
                # temp_flow['vhost_thread'] = _vm_info['vhost_thread']

                temp_flow['src_mac'] = src_macs[i]
                temp_flow['dst_mac'] = dst_macs[i]
                temp_flow['vlan'] = vlan_id[self.config['vlans']]
                src_ip = src_ip_sections[i]
                dst_ip = dst_ip_sections[i]
                temp_flow['src_ip'] = src_ip
                temp_flow['dst_ip'] = dst_ip
                vm_index = sorted(self.vms).index(_vm)
                for _queue in range(1, int(self.config['queues']) + 1):
                    # flow info
                    temp_flow['queue'] = _queue
                    # fwd thread

                    temp_flow['qemu_thread_list'] = _vm_info['qemu_thread']
                    forward_core = {
                        "forward": _vm_info['qemu_thread'][
                            _queue + avg_flow * vm_index],
                        "reverse": _vm_info['qemu_thread'][
                            _queue + avg_flow * vm_index + int(
                                self.config['flows'])]}
                    temp_flow['fwd_thread'] = forward_core[_direct]

                    temp_flow['fwd_vhost'] = None
                    # nic interrupts info
                    temp_flow['src_recv_irq'] = src_nic_irq[j]
                    temp_flow['src_nic'] = src_nic
                    temp_flow['dst_send_irq'] = dst_nic_irq[j]
                    temp_flow['dst_nic'] = dst_nic
                    # above all
                    j += 1
                    self.init_flows[_direct + '_' + _vm + '_' +
                                    str(_queue)] = copy.deepcopy(temp_flow)
                i += 1
            src_nic_irq, dst_nic_irq = dst_nic_irq, src_nic_irq
            vlan = dst_vlan
            send_port, recv_port = recv_port, send_port
            src_nic, dst_nic = dst_nic, src_nic
            src_macs, dst_macs = dst_macs, src_macs
            src_ip_sections, dst_ip_sections = dst_ip_sections, src_ip_sections
        # return sorted(self.init_flows.iteritems(), key=lambda d:d[0])
        return self.init_flows

    def mac_learning(self, flowa, flowb):
        flowa = str(flowa)
        flowb = str(flowb)
        ret = self.send_instace.mac_learning(flowa, flowb)
        return ret

    def send_packet(self, flow):
        flow = str(flow)
        # return a stream block handle
        return self.send_instace.send_packet(flow)

    def stop_flow(self, streamblock, flow):
        flow = str(flow)
        return self.send_instace.stop_flow(streamblock, flow)

    def catch_thread_info(self):
        return self.host_instance.catch_thread_info()

    def set_thread2flow(self, thread_info, flow):
        flow['fwd_vhost'] = thread_info['fwd_vhost']
        return True

    @property
    def flow_build(self):
        for _direct in fwd[self.config['direct']]:
            for _vm in self.vms:
                for _queue in range(1, int(self.config['queues']) + 1):
                    i = 0
                    while i < 50:
                        try:
                            i += 1
                            thread_info = None
                            self.mac_learning(
                                self.init_flows[
                                    _direct +
                                    '_' +
                                    _vm +
                                    '_' +
                                    str(_queue)],
                                self.init_flows[
                                    reverse_dict[_direct] +
                                    '_' +
                                    _vm +
                                    '_' +
                                    str(_queue)])
                            streamblock = self.send_packet(
                                self.init_flows[_direct + '_' + _vm + '_' + str(_queue)])
                            time.sleep(1)
                            result, thread_info = self.catch_thread_info()
                            thread_info = eval(thread_info)
                            self.stop_flow(
                                streamblock, self.init_flows[
                                    _direct + '_' + _vm + '_' + str(_queue)])
                            time.sleep(1)
                            if not result:
                                print("[ERROR]Catch the thread info failed.")
                                break
                        except:
                            print(
                                "[ERROR]send flow failed error or get host thread info failed.")

                        # compare the got thread info to
                        if check_dict(
                            thread_info, self.init_flows[
                                _direct + '_' + _vm + '_' + str(_queue)]):
                            self.set_thread2flow(
                                thread_info, self.init_flows[
                                    _direct + '_' + _vm + '_' + str(_queue)])
                            print(
                                "[INFO]Flow %s_%s_%s :     fwd_vhost %s    src_recv_irq %s   dst_send_irq %s" %
                                (_direct,
                                 _vm,
                                 _queue,
                                 thread_info['fwd_vhost'],
                                    thread_info['src_recv_irq'],
                                    thread_info['dst_send_irq']))
                            print(
                                "%s" %
                                (self.init_flows[
                                    _direct +
                                    '_' +
                                    _vm +
                                    '_' +
                                    str(_queue)]))
                            break
                        else:
                            dst_ip_update(
                                self.init_flows[
                                    _direct +
                                    '_' +
                                    _vm +
                                    '_' +
                                    str(_queue)])
        return self.init_flows

    def affinity_bind(self, aff_strategy):
        # get the forward cores
        qemu_list = []
        qemu_other = []
        src_vhost = []
        dst_vhost = []
        src_irq = []
        dst_irq = []

        # recognize the thread id
        for flowname in sorted(self.init_flows.keys()):
            tmp_thread = self.init_flows[flowname]['fwd_thread']
            qemu_other = qemu_other + \
                copy.deepcopy(self.init_flows[flowname]['qemu_thread_list'])
            qemu_list.append(tmp_thread)
            if self.init_flows[flowname]['direct'] == 'forward':
                dst_vhost.append(self.init_flows[flowname]['fwd_vhost'])
                src_irq.append(self.init_flows[flowname]['src_recv_irq'])
                dst_irq.append(self.init_flows[flowname]['dst_send_irq'])
            elif self.init_flows[flowname]['direct'] == 'reverse':
                src_vhost.append(self.init_flows[flowname]['fwd_vhost'])
                dst_irq.append(self.init_flows[flowname]['src_recv_irq'])
                src_irq.append(self.init_flows[flowname]['dst_send_irq'])

        qemu_list = sorted({}.fromkeys(qemu_list).keys())
        src_vhost = sorted({}.fromkeys(src_vhost).keys())
        dst_vhost = sorted({}.fromkeys(dst_vhost).keys())
        src_irq = sorted({}.fromkeys(src_irq).keys())
        dst_irq = sorted({}.fromkeys(dst_irq).keys())

        # get the qemu thread except the forward core
        qemu_other = sorted({}.fromkeys(qemu_other).keys())
        for i in qemu_list:
            qemu_other.remove(i)
        # get the bind strategy
        handle = ConfigParser.ConfigParser()
        handle.read(self.config['strategyfile'])
        try:
            qemu_numa = handle.get(
                'strategy' +
                self.config['strategy'],
                'qemu_numa')
            src_vhost_numa = handle.get(
                'strategy' + self.config['strategy'],
                'src_vhost_numa')
            dst_vhost_numa = handle.get(
                'strategy' + self.config['strategy'],
                'dst_vhost_numa')
            src_irq_numa = handle.get(
                'strategy' +
                self.config['strategy'],
                'src_irq_numa')
            dst_irq_numa = handle.get(
                'strategy' +
                self.config['strategy'],
                'dst_irq_numa')
            loan_numa = handle.get(
                'strategy' +
                self.config['strategy'],
                'loan_numa')
        except:
            print("[ERROR]Parse the strategy file failed or get the options failed.")

        for value in [
                qemu_numa,
                src_vhost_numa,
                dst_vhost_numa,
                src_irq_numa,
                dst_irq_numa,
                loan_numa]:
            if value is not None or value == '':
                raise ValueError('some option in the strategy file is none.')
        # cores mapping thread
        numa_topo = self.host_instance.get_numa_core()
        numa_topo = eval(numa_topo)
        # first check the cores number

        # order src_irq dst_irq src_vhost dst_vhost qemu_list
        for node in numa_topo.keys():
            numa_topo[node]['process'] = []
            if 'node' + src_irq_numa == node:
                numa_topo[node]['process'] = numa_topo[
                    node]['process'] + src_irq
            if 'node' + dst_irq_numa == node:
                numa_topo[node]['process'] = numa_topo[
                    node]['process'] + dst_irq
            if 'node' + src_vhost_numa == node:
                numa_topo[node]['process'] = numa_topo[
                    node]['process'] + src_vhost
            if 'node' + dst_vhost_numa == node:
                numa_topo[node]['process'] = numa_topo[
                    node]['process'] + dst_vhost
            if 'node' + qemu_numa == node:
                numa_topo[node]['process'] = numa_topo[
                    node]['process'] + qemu_list
        loan_cores = ''
        for node in numa_topo.keys():
            if len(
                    numa_topo[node]['process']) > len(
                    numa_topo[node]['phy_cores']):
                # length distance
                diff = len(numa_topo[node]['process']) - \
                    len(numa_topo[node]['phy_cores'])
                # first deep copy
                numa_topo['node' + loan_numa]['process'] = numa_topo['node' + loan_numa][
                    'process'] + copy.deepcopy(numa_topo[node]['process'][-diff:])
                cores_str = _tranfer_array_to_range(
                    numa_topo[
                        'node' +
                        loan_numa]['phy_cores'][
                        diff:])
                loan_cores = ','.join([loan_cores, cores_str])
                numa_topo[node]['process'] = numa_topo[
                    node]['process'][0:-diff]
        loan_cores = loan_cores[1:]
        loan_bind_list = {}
        for proc_loan in qemu_other:
            loan_bind_list[proc_loan] = loan_cores

        bind_list = {}
        for node in numa_topo.keys():
            for i in range(len(numa_topo[node]['process'])):
                bind_list[numa_topo[node]['process'][i]] = str(
                    numa_topo[node]['phy_cores'][i])
        bind_list.update(loan_bind_list)
        for key in bind_list.keys():
            self.host_instance.bind_cpu(bind_list[key], key)
        print bind_list
        return True

    def testrun(self, suite):
        global forward_init_flows, reverse_init_flows
        try:
            forward_init_flows = {}
            reverse_init_flows = {}
            for key in self.init_flows.keys():
                if self.init_flows[key]['direct'] == "forward":
                    forward_init_flows[key] = self.init_flows[key]
                elif self.init_flows[key]['direct'] == "reverse":
                    reverse_init_flows[key] = self.init_flows[key]
            forward_init_flows = str(forward_init_flows)
            reverse_init_flows = str(reverse_init_flows)
        except:
            print("[ERROR]init the forward and reverse flow failed.")

        if suite == "throughput":
            print("[INFO]!!!!!!!!!!!!!!!Now begin to throughput test")
            ret, result = self.send_instace.run_rfc2544_throughput(
                forward_init_flows, reverse_init_flows)
        elif suite == "frameloss":
            print("[INFO]!!!!!!!!!!!1!!!Now begin to frameloss test")
            ret, result = self.send_instace.run_rfc2544_frameloss(
                forward_init_flows, reverse_init_flows)
        return ret, result
