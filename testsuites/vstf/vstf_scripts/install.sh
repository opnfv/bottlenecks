#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

SERVER=$2
PORT=$3
if [ -e $SERVER ]
then
    SERVER=""
    echo "Use Default server."
fi

if [ -e $PORT ]
then
    PORT=""
    echo "Use Default port."
fi


killall vnstat
killall netserver
killall netperf
killall sar
rm -rf vstf.egg-info || exit 1
rm -rf build/ || exit 1
rm -rf /usr/local/lib/python2.7/dist-packages/vstf* || exit 1
python setup.py install --force
if [ $1 == "manager" ]; then
    vstf-agent stop
    vstf-manager stop
    if [ "${SERVER}x" == "x" ]
    then
        vstf-manager start
    else
        if [ "${PORT}x" == "x" ]; then
            vstf-manager start --monitor ${SERVER}
        else
            vstf-manager start --monitor ${SERVER} --port ${PORT}
        fi
    fi
elif [ $1 == "agent" ];then
    vstf-manager stop
    vstf-agent stop
    vstf-agent start --config_file=/etc/vstf/amqp/amqp.ini
fi
