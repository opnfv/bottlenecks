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
node REPLACED_MYSQL_NODES {
  include rubbos_mysql::rubbos_mysql_off
  include rubbos_monitor::rubbos_monitor_off
}

# tomcat node:
node REPLACED_TOMCAT_NODES {
  include rubbos_tomcat::rubbos_tomcat_off
  include rubbos_monitor::rubbos_monitor_off
}

# httpd node:
node REPLACED_HTTPD_NODES {
  include rubbos_httpd::rubbos_httpd_off
  include rubbos_monitor::rubbos_monitor_off
}

# clients
node REPLACED_CLIENT_NODES {
  include rubbos_monitor::rubbos_monitor_off
  include rubbos_client::rubbos_client_off
}
