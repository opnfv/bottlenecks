#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh

echo "Uninstalling ...."

ssh $BENCHMARK_HOST /tmp/BENCHMARK_uninstall.sh
ssh $CLIENT1_HOST /tmp/CLIENT1_uninstall.sh
ssh $CLIENT2_HOST /tmp/CLIENT2_uninstall.sh
ssh $CLIENT3_HOST /tmp/CLIENT3_uninstall.sh
ssh $CLIENT4_HOST /tmp/CLIENT4_uninstall.sh
ssh $HTTPD_HOST /tmp/HTTPD_uninstall.sh
ssh $TOMCAT1_HOST /tmp/TOMCAT1_uninstall.sh
ssh $MYSQL1_HOST /tmp/MYSQL1_uninstall.sh

echo "Cleaning up ...."
for i in "$BENCHMARK_HOST" "$CLIENT1_HOST" "$CLIENT2_HOST" "$CLIENT3_HOST" "$CLIENT4_HOST" "$HTTPD_HOST" "$TOMCAT1_HOST" "$MYSQL1_HOST"
do
  ssh $i "
    sudo \rm -r $RUBBOS_TOP
    "
done


ssh $CONTROL_HOST  rm -f /tmp/CONTROL_checkScp_exec.sh
ssh $CONTROL_HOST  rm -f /tmp/CONTROL_emulabConf_exec.sh
ssh $CONTROL_HOST  rm -f /tmp/CONTROL_rubbos_exec.sh
ssh $BENCHMARK_HOST  rm -f /tmp/BENCHMARK_rubbos_install.sh
ssh $BENCHMARK_HOST  rm -f /tmp/BENCHMARK_install.sh
ssh $BENCHMARK_HOST  rm -f /tmp/BENCHMARK_configure.sh
ssh $BENCHMARK_HOST  rm -f /tmp/BENCHMARK_uninstall.sh
ssh $BENCHMARK_HOST  rm -f /tmp/BENCHMARK_rubbos_uninstall.sh
ssh $CLIENT1_HOST  rm -f /tmp/CLIENT1_rubbos_install.sh
ssh $CLIENT1_HOST  rm -f /tmp/CLIENT1_install.sh
ssh $CLIENT1_HOST  rm -f /tmp/CLIENT1_configure.sh
ssh $CLIENT1_HOST  rm -f /tmp/CLIENT1_uninstall.sh
ssh $CLIENT1_HOST  rm -f /tmp/CLIENT1_rubbos_uninstall.sh
ssh $CLIENT2_HOST  rm -f /tmp/CLIENT2_rubbos_install.sh
ssh $CLIENT2_HOST  rm -f /tmp/CLIENT2_install.sh
ssh $CLIENT2_HOST  rm -f /tmp/CLIENT2_configure.sh
ssh $CLIENT2_HOST  rm -f /tmp/CLIENT2_uninstall.sh
ssh $CLIENT2_HOST  rm -f /tmp/CLIENT2_rubbos_uninstall.sh
ssh $CLIENT3_HOST  rm -f /tmp/CLIENT3_rubbos_install.sh
ssh $CLIENT3_HOST  rm -f /tmp/CLIENT3_install.sh
ssh $CLIENT3_HOST  rm -f /tmp/CLIENT3_configure.sh
ssh $CLIENT3_HOST  rm -f /tmp/CLIENT3_uninstall.sh
ssh $CLIENT3_HOST  rm -f /tmp/CLIENT3_rubbos_uninstall.sh
ssh $CLIENT4_HOST  rm -f /tmp/CLIENT4_rubbos_install.sh
ssh $CLIENT4_HOST  rm -f /tmp/CLIENT4_install.sh
ssh $CLIENT4_HOST  rm -f /tmp/CLIENT4_configure.sh
ssh $CLIENT4_HOST  rm -f /tmp/CLIENT4_uninstall.sh
ssh $CLIENT4_HOST  rm -f /tmp/CLIENT4_rubbos_uninstall.sh
ssh $HTTPD_HOST  rm -f /tmp/HTTPD_install.sh
ssh $HTTPD_HOST  rm -f /tmp/HTTPD_rubbos_install.sh
ssh $HTTPD_HOST  rm -f /tmp/HTTPD_configure.sh
ssh $HTTPD_HOST  rm -f /tmp/HTTPD_ignition.sh
ssh $HTTPD_HOST  rm -f /tmp/HTTPD_stop.sh
ssh $HTTPD_HOST  rm -f /tmp/HTTPD_rubbos_uninstall.sh
ssh $HTTPD_HOST  rm -f /tmp/HTTPD_uninstall.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_install.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_rubbos_install.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_configure.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_rubbosSL_configure.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_ignition.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_stop.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_rubbos_uninstall.sh
ssh $TOMCAT1_HOST  rm -f /tmp/TOMCAT1_uninstall.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_install.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_rubbos_install.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_configure.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_reset.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_ignition.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_stop.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_rubbos_uninstall.sh
ssh $MYSQL1_HOST  rm -f /tmp/MYSQL1_uninstall.sh
