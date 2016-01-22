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

import stevedore
from vstf.controller.spirent.common.result_analysis import analysis_instance as analysis_instance
LOG = logging.getLogger(__name__)


class spirentSTC(object):
    def __init__(self):
        super(spirentSTC, self).__init__()
        self.runmodel = None

    def init(self, conner="", measurand="", model="", **kwargs):
        """
        :param str    conner: the spirent tester, the agent id of spirent vm
        :param list   measurand: the tested host's agent id
        :param str    model: the model used of the tested host
        
        """
        mgr = stevedore.driver.DriverManager(namespace="spirent.model.plugins",
                                             name=model,
                                             invoke_on_load=False)
        self.TempMod = mgr.driver(kwargs)
        self.conner = conner
        self.measurand = measurand

    @property
    def run(self):
        LOG.info(vars(self.runmodel))
        return True


def run(config):
    # test option parser 
    if not os.path.exists(config['configfile']):
        LOG.error('The config file %s does exist.', config.get("configfile"))
        return False

    runmodel = None  # Tnv_Model(config = config)

    # check parameter valid
    flag = runmodel.check_parameter_invalid()
    if not flag:
        LOG.error("[ERROR]Check parameter invalid.")
        return False

    # check logical parameter in the 
    flag = runmodel.check_logic_invalid
    if not flag:
        LOG.error("[ERROR]Check logic parameter with host invalid.")
        return False

    init_flows_tables = runmodel.read_flow_init
    LOG.info(init_flows_tables)

    # print init_flows_tables
    update_flows = runmodel.flow_build
    # print update_flows
    LOG.info(update_flows)

    flag = runmodel.affinity_bind(aff_strategy=1)
    if not flag:
        LOG.error("runmodel affinity bind failed.")
        return False

    # Get the result
    result = {}
    for suite in ["frameloss", "throughput"]:
        ret, test_result = runmodel.Test_Run(suite)
        if not ret:
            LOG.error("[ERROR]Run rfc2544 %s test failed.", suite)
            return False
        try:
            ret, result_dict = restrucData(test_result)
        except:
            LOG.error("[ERROR]Restructure the test data failed.")
        perfdata = getResult(result_dict)
        columndata = getResultColumn(result_dict)
        column_array, data_array = analysis_instance.analyseResult(suite, columndata, perfdata)
        temp = {'columns': column_array, 'data': data_array}
        result[suite] = temp
    return result


if __name__ == "__main__":
    run(None)
