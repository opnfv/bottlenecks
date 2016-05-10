##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


node default { }

# mysql node:
node /.*rubbos[-|_]mysql.*/ {
  include rubbos_common::rubbos_common_on
  include rubbos_mysql::rubbos_mysql_on
  include rubbos_monitor::rubbos_monitor_on
}

# tomcat node:
node /.*rubbos[-|_]tomcat.*/ {
  include rubbos_common::rubbos_common_on
  include rubbos_tomcat::rubbos_tomcat_on
  include rubbos_monitor::rubbos_monitor_on
}

# httpd node:
node /.*rubbos[-|_]httpd.*/ {
  include rubbos_common::rubbos_common_on
  include rubbos_httpd::rubbos_httpd_on
  include rubbos_monitor::rubbos_monitor_on
}

# clients
node /.*rubbos[-|_]client.*/ {
  include rubbos_common::rubbos_common_on
  include rubbos_monitor::rubbos_monitor_on
  include rubbos_client::rubbos_client_on
}
