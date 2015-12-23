##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd. and others
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import subprocess as subp
import sys
from collector import Collector
from uploader import Uploader


#process data
if len(sys.argv)<2:
    print "no arguments, please input home directory of the output data!!!"
    exit (1)
data_home = sys.argv[1]

#1collect result
result = Collector().collect_data(data_home)
print "Result collected:\n%s" % result

#2upload result
Uploader().upload_result("rubbos", result)

