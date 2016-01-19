##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

SCENARIO_NAME_LEN = 16
DESC_LEN = 256
FIGURE_PATH_LEN = 128

CASE_TAG_LEN = 16
CASE_NAME_LEN = 128
DIRECTION_LEN = 128
CONF_LEN = 256

HOST_NAME_LEN = 32

CPU_INFO_LEN = 1024

NORMAL_VAR_LEN = 32
NORMAL_VAR_LEN1 = 64

SWITCH_LEN = 16
PROTOCOL_LEN = 16
PROVIDER_LEN = 16

TOOLS_LEN = 32
TYPE_LEN = 16

EXT_INFO_LEN = 256
DBPATH = "/opt/vstf/vstf.db"
# CaseTag, ScenarioName, CaseName, FigurePath, Description, Direction, Configure
CASE_INFO_LIST = [
    ['Ti-1', 'Ti', 'Ti_VM_RX_Tester-VM', 'res/', ' ', 'Tester->VM', 'tx', 'w/,wo VLAN'],
    ['Ti-2', 'Ti', 'Ti_VM_TX_VM-Tester', 'res/', ' ', 'VM->Tester', 'rx', 'w/,wo VLAN'],
    ['Ti-3', 'Ti', 'Ti_VM_RXTX_VM-Tester', 'res/', ' ', 'Tester<->VM', 'rxtx', 'w/,wo VLAN'],
    ['Ti-4', 'Ti', 'Ti_VM_RX_Tester-VM_VXLAN', 'res/', ' ', 'Tester->VM', 'tx', 'VXLAN'],
    ['Ti-5', 'Ti', 'Ti_VM_TX_VM-Tester_VXLAN', 'res/', ' ', 'VM->Tester', 'rx', 'VXLAN'],
    ['Ti-6', 'Ti', 'Ti_VM_RXTX_VM-Tester_VXLAN', 'res/', ' ', 'Tester<->VM', 'rxtx', 'VXLAN'],
    ['Tu-1', 'Tu', 'Tu_VM_RX_VM-VM', 'res/', ' ', 'Tester->VM', 'tx', 'w/,wo VLAN'],
    ['Tu-2', 'Tu', 'Tu_VM_TX_VM-VM', 'res/', ' ', 'VM->Tester', 'rx', 'w/,wo VLAN'],
    ['Tu-3', 'Tu', 'Tu_VM_RXTX_VM-VM', 'res/', ' ', 'Tester<->VM', 'rxtx', 'w/,wo VLAN'],
    ['Tu-4', 'Tu', 'Tu_VM_RX_VM-VM_VXLAN', 'res/', ' ', 'Tester->VM', 'tx', 'VXLAN'],
    ['Tu-5', 'Tu', 'Tu_VM_TX_VM-VM_VXLAN', 'res/', ' ', 'VM->Tester', 'rx', 'VXLAN'],
    ['Tu-6', 'Tu', 'Tu_VM_RXTX_VM-VM_VXLAN', 'res/', ' ', 'VM<->Tester', 'rxtx', 'VXLAN'],
    ['Tn-1', 'Tn', 'Tn_VSW_FWD_Tester-Tester', 'res/', ' ', 'Tester->Tester', 'tx', 'w/,wo VLAN'],
    ['Tn-2', 'Tn', 'Tn_VSW_FWD-BI_Tester-Tester', 'res/', ' ', 'Tester<->Tester', 'rxtx', 'w/,wo VLAN'],
    ['Tn-3', 'Tn', 'Tn_VSW_FWD_Tester-Tester_VXLAN', 'res/', ' ', 'Tester->Tester', 'tx', 'VXLAN'],
    ['Tn-4', 'Tn', 'Tn_VSW_FWD-BI_Tester-Tester_VXLAN', 'res/', ' ', 'Tester<->Tester', 'rxtx', 'VXLAN'],
    ['Tnv-1', 'Tnv', 'TnV_VSW_FWD_Tester-Tester', 'res/', ' ', 'Tester->Tester', 'tx', 'w/,wo VLAN'],
    ['Tnv-2', 'Tnv', 'TnV_VSW_FWD-BI_Tester-Tester', 'res/', ' ', 'Tester<->Tester', 'rxtx', 'w/,wo VLAN'],
    ['Tnv-3', 'Tnv', 'TnV_VSW_FWD_Tester-Tester_VXLAN', 'res/', ' ', 'Tester->Tester', 'tx', 'VXLAN'],
    ['Tnv-4', 'Tnv', 'TnV_VSW_FWD-BI_Tester-Tester_VXLAN', 'res/', ' ', 'Tester<->Tester', 'rxtx', 'VXLAN']
]
SCENARIO_INFO_LIST = [
    ['Ti', 'res/', ' '],
    ['Tu', 'res/', ' '],
    ['Tn', 'res/', ' '],
    ['Tnv', 'res/', ' '],
]
