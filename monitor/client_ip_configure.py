##############################################################################
# Copyright (c) 2018 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import fileinput
import re
import logging
import socket
import requests
from oslo_serialization import jsonutils

logger = logging.getLogger(__name__)
ip_address = socket.gethostbyname(socket.gethostname())

for line in fileinput.input(inplace=1):
    ip = "        Server \"" + str(ip_address)  +"\" \"25826\""
    line = re.sub(r'.*Server.*25826.*', r''+str(ip), line.rstrip())
    print(line)

for line in fileinput.input(inplace=1):
    ip =     "    URL \"http://"+str(ip_address)+":9103/collectd-post\""
    line = re.sub(r'.*URL.*collectd-post.*', r''+str(ip), line.rstrip())
    print(line)
