#!/usr/bin/python
import time
from spirent import stcPython

class Spirent_Tools(object):
    baseAPI = stcPython()
    def __init__(self):
        """This class provide API of Spirent
        
        """
        super(Spirent_Tools, self).__init__()
    
    def send_packet(self,flow):
        try:
            #import pdb
            #pdb.set_trace()
            flow = eval(flow)
            #stc init action
            self.baseAPI.stc_perform(' ResetConfig -config system1')
            self.baseAPI.stc_init()
            #create project
            project = self.baseAPI.stc_create_project()
            #create port
            port_handle = self.baseAPI.stc_create_port(project)
            #config port
            slot = flow['send_port'].split('/')[0]
            port = flow['send_port'].split('/')[1]
            self.baseAPI.stc_config_port_location(port_handle,flow['tester_ip'],slot,port)
            #create streamblock
            streamblock_handle = self.baseAPI.stc_create_streamblock(
                                                                 port_name  = port_handle,
                                                                 ExpectedRxPort = '',
                                                                 vlan_tag = flow['vlan'],
                                                                 srcMac = flow['src_mac'],
                                                                 dstMac = flow['dst_mac'],
                                                                 sourceAddr = flow['src_ip'],
                                                                 destAddr =flow['dst_ip']
                                                                 )
            # attach port
            port_list = [port_handle]
            self.baseAPI.stc_attach_ports(port_list)
            #start streamblock
            streamblock_list = [streamblock_handle]
            flag = self.baseAPI.stc_streamblock_start(streamblock_list)
            return str(streamblock_list).strip('[]')
        except :
            print("[ERROR]create stream block and send packet failed.")
            return False

    def mac_learning(self,flowA,flowB):
        try:
            #import pdb
            #pdb.set_trace()
            flowA = eval(flowA)
            flowB = eval(flowB)
            port_list = []
            streamblock_list = []
            #stc init action
            self.baseAPI.stc_perform(' ResetConfig -config system1')
            self.baseAPI.stc_init()
            #create project
            project = self.baseAPI.stc_create_project()
            #create port and config port 
            for flow in [ flowA,flowB ]:
                flow['port_handle'] = self.baseAPI.stc_create_port(project)
                tmp_test_ip = flow['tester_ip']
                tmp_slot = flow['send_port'].split('/')[0]
                tmp_port = flow['send_port'].split('/')[1]
                self.baseAPI.stc_config_port_location(flow['port_handle'],tmp_test_ip,tmp_slot,tmp_port)
                #create streamblock
                flow['streamblock'] = self.baseAPI.stc_create_streamblock(port_name  = flow['port_handle'],
                                                                     ExpectedRxPort = '',
                                                                     vlan_tag = flow['vlan'],
                                                                     srcMac = flow['src_mac'],
                                                                     dstMac = flow['dst_mac'],
                                                                     sourceAddr = flow['src_ip'],
                                                                     destAddr =flow['dst_ip'])
                #create port and stream block list
                port_list.append(flow['port_handle'])
                streamblock_list.append(flow['streamblock'])

            #attach port
            self.baseAPI.stc_attach_ports(port_list)
            #start streamblock
            flag = self.baseAPI.stc_streamblock_start(streamblock_list)
            # mac learning
            time.sleep(2)
            # stop stream block
            self.baseAPI.stc_streamblock_stop(streamblock_list)
            # delete streamblock and release port
            for flow in [ flowA,flowB ]:
                tmp_test_ip = flow['tester_ip']
                tmp_slot = flow['send_port'].split('/')[0]
                tmp_port = flow['send_port'].split('/')[1]
                self.baseAPI.stc_delete(flow['streamblock'])
                self.baseAPI.stc_release('%s/%s/%s' %(tmp_test_ip,tmp_slot,tmp_port))
            # delete project
            self.baseAPI.stc_delete('project1')
            ret = self.baseAPI.stc_perform('ResetConfig -config system1')
            return True
        except :
            print("[ERROR]mac learning failed")
            return False

    def stop_flow(self,streamblock_list,flow):
        flow = eval(flow)
        streamblock_list = streamblock_list.strip('\'').split(',')
        #stop streamblock list
        try :
            ret = self.baseAPI.stc_streamblock_stop(streamblock_list)
        except :
            print("[ERROR]Stop the streamblock list failed.")
            return False
        #delete streamblock
        try :
            for streamblock in streamblock_list :
                ret = self.baseAPI.stc_delete(streamblock)
        except :
            print("[ERROR]delete stream block.")
            return False
        #release port
        try :
            slot = flow['send_port'].split('/')[0]
            port = flow['send_port'].split('/')[1]
            ret = self.baseAPI.stc_release('%s/%s/%s' %(flow['tester_ip'],slot,port))
        except :
            print("[ERROR]Release port failed")
            return False
        ##delete project
        try :
            ret = self.baseAPI.stc_delete('project1')
            ret = self.baseAPI.stc_perform('ResetConfig -config system1')
            return True
        except :
            print("[ERROR]Delete project1 failed.")
            return False
        
    def run_rfc2544_throughput(self,forward_init_flows,reverse_init_flows):
        #import pdb
        #pdb.set_trace()
        #rebuild the flows 
        forward_init_flows = eval(forward_init_flows)
        reverse_init_flows = eval(reverse_init_flows)
        #stc init action
        self.baseAPI.stc_perform(' ResetConfig -config system1')
        self.baseAPI.stc_init()
        #create project 
        project = self.baseAPI.stc_create_project()
        #create sequencer
        seq_handle = self.baseAPI.stc_create('Sequencer -under %s' %(project))
        #create port handle
        forward_port_handle = self.baseAPI.stc_create_port(project)
        reverse_port_handle = self.baseAPI.stc_create_port(project)
        #create forward flow streamblock
        for key in forward_init_flows.keys():
            forward_init_flows[key]['port_handle'] = forward_port_handle
            tmp_test_ip = forward_init_flows[key]['tester_ip']
            tmp_slot    = forward_init_flows[key]['send_port'].split('/')[0]
            tmp_port    = forward_init_flows[key]['send_port'].split('/')[1]
            self.baseAPI.stc_config_port_location(forward_init_flows[key]['port_handle'],tmp_test_ip,tmp_slot,tmp_port)
            #create streamblock
            forward_init_flows[key]['streamblock'] = self.baseAPI.stc_create_streamblock(port_name  = forward_init_flows[key]['port_handle'],
                                                                                     vlan_tag   = forward_init_flows[key]['vlan'],
                                                                                     ExpectedRxPort = reverse_port_handle,
                                                                                     srcMac     = forward_init_flows[key]['src_mac'],
                                                                                     dstMac     = forward_init_flows[key]['dst_mac'],
                                                                                     sourceAddr = forward_init_flows[key]['src_ip'],
                                                                                     destAddr   = forward_init_flows[key]['dst_ip'])
        #create reverse flow streamblock
        for key in reverse_init_flows.keys():
            reverse_init_flows[key]['port_handle'] = reverse_port_handle
            tmp_test_ip = reverse_init_flows[key]['tester_ip']
            tmp_slot    = reverse_init_flows[key]['send_port'].split('/')[0]
            tmp_port    = reverse_init_flows[key]['send_port'].split('/')[1]
            self.baseAPI.stc_config_port_location(reverse_init_flows[key]['port_handle'],tmp_test_ip,tmp_slot,tmp_port)
            #create streamblock
            reverse_init_flows[key]['streamblock'] = self.baseAPI.stc_create_streamblock(port_name  = reverse_init_flows[key]['port_handle'],
                                                                                     vlan_tag   = reverse_init_flows[key]['vlan'],
                                                                                     ExpectedRxPort = forward_port_handle,
                                                                                     srcMac     = reverse_init_flows[key]['src_mac'],
                                                                                     dstMac     = reverse_init_flows[key]['dst_mac'],
                                                                                     sourceAddr = reverse_init_flows[key]['src_ip'],
                                                                                     destAddr   = reverse_init_flows[key]['dst_ip'])
        #Create the RFC 2544 throughput test
        throughput_config = self.baseAPI.stc_create('Rfc2544ThroughputConfig -under ',project,
                                                '-AcceptableFrameLoss 0.01',
                                                '-NumOfTrials 1',
                                                '-DurationSeconds 60',
                                                '-SearchMode BINARY',
                                                '-RateLowerLimit 1',
                                                '-RateUpperLimit 100',
                                                '-RateInitial 10',
                                                '-UseExistingStreamBlocks True',
                                                '-EnableLearning False',
                                                '-FrameSizeIterationMode CUSTOM',
                                                '-CustomFrameSizeList "70 128 256 512 1024 1280 1518"',
                                                '-LatencyType LIFO',
                                                '-EnableJitterMeasurement TRUE'
                                                )
        #import pdb
        #pdb.set_trace()
        # list streamblocks
        streamblock_list = '" '
        for key in forward_init_flows.keys():
            streamblock_list = streamblock_list+forward_init_flows[key]['streamblock']+' '
        for key in reverse_init_flows.keys():
            streamblock_list = streamblock_list+reverse_init_flows[key]['streamblock']+' '
        streamblock_list = streamblock_list+'"'

        throughput_sbProfile= self.baseAPI.stc_create('Rfc2544StreamBlockProfile -under '+throughput_config+' -Active TRUE -LocalActive TRUE')
        self.baseAPI.stc_config(throughput_sbProfile,'-StreamBlockList '+streamblock_list)
        self.baseAPI.stc_perform('ExpandBenchmarkConfigCommand','-config ',throughput_config)

        #attach the port before testing
        port_list = [ forward_port_handle,reverse_port_handle]
        self.baseAPI.stc_attach_ports(port_list)

        #stc apply and begin to sequence test
        self.baseAPI.stc_apply()
        self.baseAPI.stc_perform("SequencerStart")

        #wait until complete
        self.baseAPI.stc_waituntilcomplete()
        
        #get result db
        resultsdb = self.baseAPI.stc_get("system1.project.TestResultSetting", "-CurrentResultFileName")
        results_dict = self.baseAPI.stc_perform('QueryResult','-DatabaseConnectionString',resultsdb,'-ResultPath RFC2544ThroughputTestResultDetailedSummaryView')
        #print results_dict
        return True,results_dict

    def run_rfc2544_frameloss(self,forward_init_flows,reverse_init_flows):
        #import pdb
        #pdb.set_trace()
        #rebuild the flows
        forward_init_flows = eval(forward_init_flows)
        reverse_init_flows = eval(reverse_init_flows)
        #stc init action
        self.baseAPI.stc_perform(' ResetConfig -config system1')
        self.baseAPI.stc_init()
        #create project
        project = self.baseAPI.stc_create_project()
        #create sequencer
        seq_handle = self.baseAPI.stc_create('Sequencer -under %s' %(project))
        #create port handle
        forward_port_handle = self.baseAPI.stc_create_port(project)
        reverse_port_handle = self.baseAPI.stc_create_port(project)
        #create forward flow streamblock
        for key in forward_init_flows.keys():
            forward_init_flows[key]['port_handle'] = forward_port_handle
            tmp_test_ip = forward_init_flows[key]['tester_ip']
            tmp_slot    = forward_init_flows[key]['send_port'].split('/')[0]
            tmp_port    = forward_init_flows[key]['send_port'].split('/')[1]
            self.baseAPI.stc_config_port_location(forward_init_flows[key]['port_handle'],tmp_test_ip,tmp_slot,tmp_port)
            #create streamblock
            forward_init_flows[key]['streamblock'] = self.baseAPI.stc_create_streamblock(port_name  = forward_init_flows[key]['port_handle'],
                                                                                     vlan_tag   = forward_init_flows[key]['vlan'],
                                                                                     ExpectedRxPort = reverse_port_handle,
                                                                                     srcMac     = forward_init_flows[key]['src_mac'],
                                                                                     dstMac     = forward_init_flows[key]['dst_mac'],
                                                                                     sourceAddr = forward_init_flows[key]['src_ip'],
                                                                                     destAddr   = forward_init_flows[key]['dst_ip'])
        #create reverse flow streamblock
        for key in reverse_init_flows.keys():
            reverse_init_flows[key]['port_handle'] = reverse_port_handle
            tmp_test_ip = reverse_init_flows[key]['tester_ip']
            tmp_slot    = reverse_init_flows[key]['send_port'].split('/')[0]
            tmp_port    = reverse_init_flows[key]['send_port'].split('/')[1]
            self.baseAPI.stc_config_port_location(reverse_init_flows[key]['port_handle'],tmp_test_ip,tmp_slot,tmp_port)
            #create streamblock
            reverse_init_flows[key]['streamblock'] = self.baseAPI.stc_create_streamblock(port_name  = reverse_init_flows[key]['port_handle'],
                                                                                     vlan_tag   = reverse_init_flows[key]['vlan'],
                                                                                     ExpectedRxPort = forward_port_handle,
                                                                                     srcMac     = reverse_init_flows[key]['src_mac'],
                                                                                     dstMac     = reverse_init_flows[key]['dst_mac'],
                                                                                     sourceAddr = reverse_init_flows[key]['src_ip'],
                                                                                     destAddr   = reverse_init_flows[key]['dst_ip'])
        #Create the RFC 2544 frameloss test
        frameloss_config = self.baseAPI.stc_create('Rfc2544FrameLossConfig -under ',project,
                                                '-NumOfTrials 1 ',
                                                '-DurationSeconds 60 ',
                                                '-LoadUnits PERCENT_LINE_RATE ',
                                                '-LoadType CUSTOM '
                                                '-CustomLoadList 100 '
                                                '-UseExistingStreamBlocks True ',
                                                '-EnableLearning False ',
                                                '-FrameSizeIterationMode CUSTOM ',
                                                '-CustomFrameSizeList "70 128 256 512 1024 1280 1518"',
                                                '-LatencyType LIFO',
                                                '-EnableJitterMeasurement TRUE'
                                                )
        #import pdb
        #pdb.set_trace()
        # list streamblocks
        streamblock_list = '" '
        for key in forward_init_flows.keys():
            streamblock_list = streamblock_list+forward_init_flows[key]['streamblock']+' '
        for key in reverse_init_flows.keys():
            streamblock_list = streamblock_list+reverse_init_flows[key]['streamblock']+' '
        streamblock_list = streamblock_list+'"'

        frameloss_sbProfile= self.baseAPI.stc_create('Rfc2544StreamBlockProfile -under '+frameloss_config+' -Active TRUE -LocalActive TRUE')
        self.baseAPI.stc_config(frameloss_sbProfile,'-StreamBlockList '+streamblock_list)
        self.baseAPI.stc_perform('ExpandBenchmarkConfigCommand','-config ',frameloss_config)

        #attach the port before testing
        port_list = [ forward_port_handle,reverse_port_handle]
        self.baseAPI.stc_attach_ports(port_list)

        #stc apply and begin to sequence test
        self.baseAPI.stc_apply()
        self.baseAPI.stc_perform("SequencerStart")

        #wait until complete
        self.baseAPI.stc_waituntilcomplete()

        #get result db
        resultsdb = self.baseAPI.stc_get("system1.project.TestResultSetting", "-CurrentResultFileName")
        results_dict = self.baseAPI.stc_perform('QueryResult','-DatabaseConnectionString',resultsdb,'-ResultPath RFC2544FrameLossTestResultDetailedSummaryView')
        #import pdb
        #pdb.set_trace()
        return True,results_dict

    def run_rfc2544_latency(self,forward_init_flows,reverse_init_flows):
        pass

