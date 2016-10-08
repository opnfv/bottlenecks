##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.rpc_frame_work import constant as const
import vstf.common.constants as cst


class Fabricant(object):

    def __init__(self, target, conn):
        self.conn = conn
        self.target = target

        self.all_commands = self.declare_commands
        self.instance_commands()

    @property
    def declare_commands(self):
        driver = {
            "install_drivers",
            "clean_drivers",
            "autoneg_on",
            "autoneg_off",
            "autoneg_query"}

        builder = {"build_env", "clean_env"}

        cpu = {"affctl_load", "affctl_list", "run_cpuwatch", "kill_cpuwatch"}

        perf = {"perf_run", "run_vnstat", "kill_vnstat", "force_clean"}

        device_mgr = {
            "get_device_detail",
            "list_nic_devices",
            "get_device_verbose"}

        netns = {"clean_all_namespace", "config_dev", "recover_dev", "ping"}

        collect = {"collect_host_info"}

        cmdline = {"execute"}

        spirent = {
            "send_packet",
            "stop_flow",
            "mac_learning",
            "run_rfc2544suite",
            "run_rfc2544_throughput",
            "run_rfc2544_frameloss",
            "run_rfc2544_latency"}

        equalizer = {
            "get_numa_core",
            "get_nic_numa",
            "get_nic_interrupt_proc",
            "get_vm_info",
            "bind_cpu",
            "catch_thread_info"}

        return driver | cpu | builder | perf | device_mgr | netns | cmdline | collect | spirent | equalizer

    def instance_commands(self):
        for command in self.all_commands:
            setattr(self, command, self.__transfer_msg(command))

    def __transfer_msg(self, command):
        def infunc(timeout=cst.TIMEOUT, **kwargs):
            msg = self.conn.make_msg(command, **kwargs)
            if self.target:
                return self.conn.call(msg, self.target, timeout)
            return None

        infunc.__name__ = command
        return infunc
