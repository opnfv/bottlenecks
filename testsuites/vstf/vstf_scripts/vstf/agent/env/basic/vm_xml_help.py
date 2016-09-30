##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

xml_head = '''
<domain type='kvm'>
  <name>VM_NAME</name>
  <memory unit='KiB'>VM_MEMORY</memory>
  <currentMemory unit='KiB'>VM_MEMORY</currentMemory>
  <!--numatune>
       <memory mode='strict' nodeset='0'/>
  </numatune-->
  <vcpu placement='static'>CPU_NUM</vcpu>
  <cpu mode='host-passthrough'>
  </cpu>
  <os>
    <type arch='x86_64' >hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>'''
xml_disk = '''
    <disk type='file' device='disk'>
      <driver name='qemu' type='IMAGE_TYPE' cache='none' io='native'/>
      <source file='IMAGE_PATH'/>
      <target dev='vda' bus='virtio'/>
    </disk>'''

xml_ctrl_br = '''
<interface type='bridge'>
  <mac address='CTRL_MAC'/>
  <source bridge='CTRL_BR'/>
  <model type='CTRL_MODEL'/>
</interface>
'''
xml_ovs = '''
    <interface type='bridge'>
      <mac address='TAP_MAC'/>
      <source bridge='BR_NAME'/>
      <virtualport type='BR_TYPE'>
      </virtualport>
      <model type='virtio'/>
      <driver name='vhost' queues='4'/>
      <target dev='TAP_NAME'/>
    </interface>'''
xml_br = '''
    <interface type='bridge'>
      <mac address='TAP_MAC'/>
      <source bridge='BR_NAME'/>
      <model type='virtio'/>
      <target dev='TAP_NAME'/>
    </interface>'''

xml_pci = '''
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <driver name='kvm'/>
      <source>
        <address domain='0x0000' bus='0xBUS' slot='0xSLOT' function='0xFUNCTION' />
      </source>
    </hostdev>'''
xml_9p = '''
    <filesystem type='mount' accessmode='passthrough'>
      <source dir='9P_PATH'/>
      <target dir='9pfs'/>
    </filesystem>'''
xml_tail = '''
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
  </devices>
</domain>'''
