##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from vstf.agent.spirent.tools import Spirent_Tools as Spirent


class agentSpirent(Spirent):

    def __init__(self):
        super(agentSpirent, self).__init__()
