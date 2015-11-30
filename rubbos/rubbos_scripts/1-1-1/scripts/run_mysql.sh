#!/bin/bash


ssh $MYSQL1_HOST /tmp/MYSQL1_install.sh 




ssh $MYSQL1_HOST /tmp/MYSQL1_rubbos_install.sh 




ssh $MYSQL1_HOST /tmp/MYSQL1_configure.sh  &
sleep 60


#ssh $CONTROL_HOST /tmp/CONTROL_rubbos_exec.sh 

