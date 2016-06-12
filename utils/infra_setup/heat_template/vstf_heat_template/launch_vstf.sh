#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -x

STACK_NAME="bottlenecks_vstf_stack"
VM_MANAGER_USER="root"
VM_MANAGER_PASSWD="root"
VM_TARGET_USER="root"
VM_TARGET_PASSWD="root"
VM_TESTER_USER="root"
VM_TESTER_PASSWD="root"
RABBITMQ_PORT="5672"

#load func
#source ./ssh.sh
#source ./scp.sh

function fn_parser_ipaddress(){
    #parser and get output ipaddress
    manager_control_private_ip=`heat output-show ${STACK_NAME} manager_control_private_ip | sed 's/\"//g'`
    manager_control_public_ip=`heat output-show ${STACK_NAME} manager_control_public_ip | sed 's/\"//g'`
    echo "manager_control_private_ip = ${manager_control_private_ip}"
    #ping -c 5 ${manager_control_private_ip}
    echo "manager_control_public_ip = ${manager_control_public_ip}"
    ping -c 5 ${manager_control_public_ip}
    target_control_private_ip=`heat output-show ${STACK_NAME} target_control_private_ip | sed 's/\"//g'`
    target_control_public_ip=`heat output-show ${STACK_NAME} target_control_public_ip | sed 's/\"//g'`
    echo "target_control_private_ip = ${target_control_private_ip}"
    #ping -c 5 ${target_control_private_ip}
    echo "target_control_public_ip = ${target_control_public_ip}"
    ping -c 5 ${target_control_public_ip}
    tester_control_private_ip=`heat output-show ${STACK_NAME} tester_control_private_ip | sed 's/\"//g'`
    tester_control_public_ip=`heat output-show ${STACK_NAME} tester_control_public_ip | sed 's/\"//g'`
    echo "tester_control_private_ip = ${tester_control_private_ip}"
    #ping -c 5 ${tester_control_private_ip}
    echo "tester_control_public_ip = ${tester_control_public_ip}"
    ping -c 5 ${tester_control_public_ip}

    #get testing ipaddress
    tester_testing_ip=`nova list | grep "vstf-tester" | grep "bottlenecks-testing" | awk -F'bottlenecks-testing=' '{print $2}' | awk '{print $1}'`
    target_testing_ip=`nova list | grep "vstf-target" | grep "bottlenecks-testing" | awk -F'bottlenecks-testing=' '{print $2}' | awk '{print $1}'`
    echo "tester_testing_ip = ${tester_testing_ip}"
    echo "target_testing_ip = ${target_testing_ip}"
    
    #config ip for the testing plane
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${target_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${target_control_public_ip} "ifconfig eth1 ${target_testing_ip}/24;sleep 4"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${tester_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${tester_control_public_ip} "ifconfig eth1 ${tester_testing_ip}/24;sleep 4"
    #ping with each other
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${target_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${target_control_public_ip} "ping -c 10 ${tester_testing_ip}"
    
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${tester_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${tester_control_public_ip} "ping -c 10 ${target_testing_ip}"

    local ipaddr=""
    for ipaddr in ${manager_control_private_ip} ${manager_control_public_ip} ${target_control_private_ip} \
                  ${target_control_public_ip} ${tester_control_private_ip} ${tester_control_public_ip}
    do
        if [ "${ipaddr}x" == "x" ]
        then
            echo "[ERROR]The ipaddress is null ,get ip from heat output failed"
            exit 1
        fi
    done

    return 0
}

function fn_generate_amqp(){
    local node_type=$1
    if [ "${node_type}" == "manager" ]
    then
        return 0
    elif [ "${node_type}" == "target" -o "${node_type}" == "tester" ]
    then
        echo "[rabbit]" > ./vstf-${node_type}.ini
        echo "user=guest" >> ./vstf-${node_type}.ini
        echo "passwd=guest" >> ./vstf-${node_type}.ini
        echo "host=${manager_control_private_ip}" >> ./vstf-${node_type}.ini
        echo "port=${RABBITMQ_PORT}" >> ./vstf-${node_type}.ini
        echo "id=\"${node_type}\"" >> ./vstf-${node_type}.ini
    else
        echo "[ERROR]node type ${node_type} does not exist"
        exit 1
    fi
    return 0
}

function fn_provision_agent_file(){

    #apt-get -y install expect
    #manager
    fn_generate_amqp "manager"
    
    #target
    fn_generate_amqp "target"
    #scp_cmd ${target_control_public_ip} ${VM_TARGET_USER} ${VM_TARGET_PASSWD} "./vstf-target.ini" "/etc/vstf/amqp/amqp.ini" "file"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${target_control_public_ip}
    sshpass -p root scp -o StrictHostKeyChecking=no "./vstf-target.ini" root@${target_control_public_ip}:/etc/vstf/amqp/amqp.ini
    #tester
    fn_generate_amqp "tester"
    #scp_cmd ${tester_control_public_ip} ${VM_TESTER_USER} ${VM_TESTER_PASSWD} "./vstf-tester.ini" "/etc/vstf/amqp/amqp.ini" "file"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${tester_control_public_ip}
    sshpass -p root scp -o StrictHostKeyChecking=no "./vstf-tester.ini" root@${tester_control_public_ip}:/etc/vstf/amqp/amqp.ini

    return 0
}

function fn_launch_vstf_process(){

    #launch manager
    local manager_cmd="vstf-manager stop;pkill vstf-manager;rm -rf /opt/vstf/vstf-server.pid;vstf-manager start --monitor ${manager_control_private_ip} --port ${RABBITMQ_PORT}"
    #run_cmd ${manager_control_public_ip} ${VM_MANAGER_USER} ${VM_MANAGER_PASSWD} "${manager_cmd}"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${manager_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${manager_control_public_ip} "ifconfig -a"
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${manager_control_public_ip} "${manager_cmd}"
    
    #launch target agent
    local target_cmd="vstf-agent stop;pkill vstf-agent;rm -rf /tmp/esp_rpc_client.pid;vstf-agent start --config_file=/etc/vstf/amqp/amqp.ini"
    #run_cmd ${target_control_public_ip} ${VM_TARGET_USER} ${VM_TARGET_PASSWD} "${target_cmd}"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${target_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${target_control_public_ip} "ifconfig -a"
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${target_control_public_ip} "${target_cmd}"
    
    #launch tester agent
    #run_cmd ${tester_control_public_ip} ${VM_TESTER_USER} ${VM_TESTER_PASSWD} "${target_cmd}"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${tester_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${tester_control_public_ip} "ifconfig -a"
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${tester_control_public_ip} "${target_cmd}"

    return 0
}

function main(){
    fn_parser_ipaddress
    fn_provision_agent_file
    fn_launch_vstf_process
    cmd="rabbitmqctl list_queues"
    sleep 20
    #${manager_control_public_ip} ${VM_MANAGER_USER} ${VM_MANAGER_PASSWD} "${cmd}"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${manager_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${manager_control_public_ip} "${cmd}"
    return 0
}

main
set +x
