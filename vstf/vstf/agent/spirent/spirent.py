##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import Tkinter


def build_cmd(*args):
    cmd = ''
    for arg in args:
        cmd = cmd+str(arg)+' '
    #import pdb
    #pdb.set_trace()
    return cmd


class stcPython():
    def __init__(self):
        self.tclsh = Tkinter.Tcl()
        self.stcpkg = '/home/Spirent_TestCenter_4.46/Spirent_TestCenter_Application_Linux'
        self.tclsh.eval("set auto_path [ linsert $auto_path 0 %s ]" %(self.stcpkg))
        self.tclsh.eval("package require SpirentTestCenter")

    def build_cmd(self, *args):
        cmd = ''
        for arg in args:
            cmd = cmd+str(arg)+' '
        return cmd

    # [ stc base interface ]
    def stc_init(self, *args):
        cmd = build_cmd('stc::init', *args)
        return self.tclsh.eval(cmd)
    # stc connect
    def stc_connect(self,*args):
        cmd = build_cmd('stc::connect', *args)
        return self.tclsh.eval(cmd)
    # stc disconnect
    def stc_disconnect(self,*args):
        cmd = build_cmd('stc::disconnect', *args)
        return self.tclsh.eval(cmd)
    # stc create
    def stc_create(self,*args):
        cmd = build_cmd('stc::create', *args)
        return self.tclsh.eval(cmd)
    # stc delete
    def stc_delete(self,*args):
        cmd = build_cmd('stc::delete', *args)
        return self.tclsh.eval(cmd)
    # stc config
    def stc_config(self,*args):
        cmd = build_cmd('stc::config', *args)
        return self.tclsh.eval(cmd)
    # stc get
    def stc_get(self,*args):
        cmd = build_cmd('stc::get', *args)
        return self.tclsh.eval(cmd)
    # stc apply
    def stc_apply(self,*args):
        cmd = build_cmd('stc::apply', *args)
        return self.tclsh.eval(cmd)
    # stc perform
    def stc_perform(self,*args):
        cmd = build_cmd('stc::perform', *args)
        return self.tclsh.eval(cmd)
    # stc reserve
    def stc_reserve(self,*args):
        cmd = build_cmd('stc::reserve', *args)
        return self.tclsh.eval(cmd)
    # stc release
    def stc_release(self,*args):
        cmd = build_cmd('stc::release', *args)
        return self.tclsh.eval(cmd)
    # stc subscribe
    def stc_subscribe(self,*args):
        cmd = build_cmd('stc::subscribe',*args)
        return self.tclsh.eval(cmd)
    # stc unsubscribe
    def stc_unsubscribe(self,*args):
        cmd = build_cmd('stc::unsubscribe', *args)
        return self.tclsh.eval(cmd)
    # stc wait until sequencer complete
    def stc_waituntilcomplete(self,*args):
        cmd = build_cmd('stc::waituntilcomplete', *args)
        return self.tclsh.eval(cmd)
    # stc help
    def stc_help(self, *args):
        cmd = build_cmd('stc::help',*args)
        return self.tclsh.eval(cmd)

    # [ stc expand interface ]
    # get one dict-key's value
    # return value
    def stc_get_value(self,stc_dict,stc_key):
        cmd = stc_dict+' -'+stc_key
        return self.stc_get(cmd)
    # create project
    # return: project_name
    def stc_create_project(self):
        return self.stc_create('project')
    # create port under project
    # return: port name
    def stc_create_port(self,project_name):
        cmd = 'port -under '+project_name
        return self.stc_create(cmd)
    # config port location
    # return: None
    def stc_config_port_location(self,port_name,chassisAddress,slot,port):
        #import pdb
        #pdb.set_trace()
        cmd = port_name+' -location //'+chassisAddress+'/'+slot+'/'+port+' -UseDefaultHost False'
        return self.stc_config(cmd)
    # create streamblock under port
    # return: streamblock name
    def stc_create_streamblock(self,port_name,vlan_tag,ExpectedRxPort,srcMac,dstMac,sourceAddr,destAddr):
        #import pdb
        #pdb.set_trace()
        if vlan_tag == None or vlan_tag == 'None':
            frameStruc = '"EthernetII IPv4 Udp"'
            if ExpectedRxPort == '' :
                return self.stc_create( 'streamBlock -under ',port_name,
                                        '-frameConfig ',frameStruc,
                                        '-frame "EthernetII.srcMac',srcMac,'EthernetII.dstMac',dstMac,
                                        'IPv4.1.sourceAddr',sourceAddr,'IPv4.1.destAddr',destAddr,'"')
            else :
                return self.stc_create( 'streamBlock -under ',port_name,
                                        '-ExpectedRxPort',ExpectedRxPort,
                                        '-frameConfig ',frameStruc,
                                        '-frame "EthernetII.srcMac',srcMac,'EthernetII.dstMac',dstMac,
                                        'IPv4.1.sourceAddr',sourceAddr,'IPv4.1.destAddr',destAddr,'"')
        else :
            frameStruc = '"EthernetII Vlan IPv4 Udp"'
            if ExpectedRxPort == '' :
                return self.stc_create( 'streamBlock -under ',port_name,
                                        '-frameConfig '+frameStruc,
                                        '-frame "EthernetII.srcMac',srcMac,'EthernetII.dstMac',dstMac,
                                        'Vlan.1.id',vlan_tag,
                                        'IPv4.1.sourceAddr',sourceAddr,'IPv4.1.destAddr',destAddr,'"')
            else :
                return self.stc_create( 'streamBlock -under ',port_name,
                                        '-ExpectedRxPort',ExpectedRxPort,
                                        '-frameConfig '+frameStruc,
                                        '-frame "EthernetII.srcMac',srcMac,'EthernetII.dstMac',dstMac,
                                        'Vlan.1.id',vlan_tag,
                                        'IPv4.1.sourceAddr',sourceAddr,'IPv4.1.destAddr',destAddr,'"')
    # config streamblock with part arguments
    # argument list use args dictionary
    def stc_config_streamblock(self,streamblock_name,args_dict):
        cmd = ''
        for key in args_dict.keys() :
            temp_cmd = '-'+key+' '+str(args_dict[key])
            cmd = cmd + temp_cmd
        return self.stc_config(streamblock_name,cmd)
    # get generator name from port name
    # return: generator name
    def stc_get_generator(self,port_name):
        cmd = port_name+' -children-generator'
        return self.stc_get(cmd)
    # config generator with part arguments
    # argument list use args dictionary
    # return none
    def stc_config_generator(self,generator_name,args_dict):
        cmd = ''
        for key in args_dict.keys() :
            temp_cmd = '-'+key+' '+str(args_dict[key])
            cmd = cmd + temp_cmd
        return self.stc_config(generator_name,cmd)
    # attach port
    # return: port's parent project info
    def stc_attach_ports(self,portList):
        cmd = 'AttachPorts -portList {'
        for port in portList :
            cmd = cmd+' '+port
        cmd = cmd+'} -autoConnect TRUE'
        return self.stc_perform(cmd)
    # config src mac and dst mac
    # return: none
    def stc_config_ethII(self,ethII,src_mac,dst_mac):
        cmd = ethII+' -srcMac '+src_mac+' -dstMac '+dst_mac
        return self.stc_config(cmd)
    # config src ip and dst ip
    # return: none
    def stc_config_ethIII(self,ethIII,src_ip,dst_ip):
        cmd = ethIII+' -sourceAddr '+src_ip+' -destAddr '+dst_ip
        return self.stc_config(cmd)
    # start streamblock
    # return: none
    def stc_streamblock_start(self,streamblock_list):
        cmd = 'StreamBlockStart -StreamBlockList {'
        for streamblock in streamblock_list :
            cmd = cmd+' '+streamblock
        cmd = cmd+' } -ExecuteSynchronous TRUE'
        return self.stc_perform(cmd)
    # stop streamblock
    def stc_streamblock_stop(self,streamblock_list):
        cmd = 'StreamBlockStop -StreamBlockList {'
        for streamblock in streamblock_list :
            cmd = cmd+' '+streamblock
        cmd = cmd+' } -ExecuteSynchronous TRUE'
        return self.stc_perform(cmd)
    # start generator
    # return: none
    def stc_generator_start(self,generator_List):
        cmd = 'GeneratorStart -generatorList {'
        for generator in generator_List :
            cmd = cmd+' '+generator
        cmd = cmd+' }'
        return self.stc_perform(cmd)
    # stop generator
    # return: none
    def stc_generator_stop(self,generator_List):
        cmd = 'GeneratorStop -generatorList {'
        for generator in generator_List :
            cmd = cmd+' '+generator
        cmd = cmd+' }'
        return self.stc_perform(cmd)
    # create rfc2544 throughput test
    def stc_setup_rfc2544_throughput(self):
        pass
    # create rfc2544 frameloss test
    def stc_setup_rfc2544_frameloss(self):
        pass
    # create rfc2544 latency test
    def stc_setup_rfc2544_latency(self):
        pass
    # start Sequence start
    def stc_sequence_start(self):
        return self.stc_perform('SequencerStart')
    # output rfc2544 throughput result
    def stc_get_rfc2544_throughput_result(self):
        pass
    # output rfc2544 frameloss result
    def stc_get_rfc2544_frameloss_result(self):
        pass
    # output rfc2544 latency result
    def stc_get_rfc2544_latency_result(self):
        pass
