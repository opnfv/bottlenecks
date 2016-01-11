#!/bin/bash
set -x

VM_MANAGER_USER="root"
VM_MANAGER_PASSWD="root"
STACK_NAME="vstf"
#load func
source ./ssh.sh
source ./scp.sh

function fn_parser_ipaddress(){
    #parser and get output ipaddress
    manager_control_private_ip=`heat output-show ${STACK_NAME} manager_control_private_ip | sed 's/\"//g'`
    manager_control_public_ip=`heat output-show ${STACK_NAME} manager_control_public_ip | sed 's/\"//g'`

    local ipaddr=""
    for ipaddr in ${manager_control_private_ip} ${manager_control_public_ip}
    do
        if [ "${ipaddr}x" == "x" ]
        then
            echo "[ERROR]The ipaddress is null ,get ip from heat output failed"
            exit 1
        fi
    done

    return 0
}

function fn_vstf_test_config(){
    #get testing ipaddress
    tester_testing_ip=`nova list | grep "vstf-tester" | grep "bottlenecks-testing" | awk -F'bottlenecks-testing=' '{print $2}' | awk '{print $1}'`
    target_testing_ip=`nova list | grep "vstf-target" | grep "bottlenecks-testing" | awk -F'bottlenecks-testing=' '{print $2}' | awk '{print $1}'`
    echo "tester_testing_ip = ${tester_testing_ip}"
    echo "target_testing_ip = ${target_testing_ip}"
    #setting testting ipaddress
    local cmd="vstfadm settings ${tester_testing_ip} ${target_testing_ip}"
    echo "$cmd"
    #run_cmd ${manager_control_public_ip} ${VM_MANAGER_USER} ${VM_MANAGER_PASSWD} "${cmd}"
    ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${manager_control_public_ip}
    sshpass -p root ssh -o StrictHostKeyChecking=no root@${manager_control_public_ip} "${cmd}"

    return 0
}

function fn_testing_scenario(){
    local head_cmd="vstfadm perf-test "
    local test_length_list="64"
    local test_scenario_list="Tu-1 Tu-3"
    local test_tool="netperf"
    local protocol="udp"
    local test_type="frameloss"
    for scene in ${test_scenario_list}
    do
        local cmd="${head_cmd} ${scene} ${test_tool} ${protocol} ${test_type} \"${test_length_list}\" > /root/${scene}-result.txt"
        echo ${cmd}

        ssh-keygen -f "/home/jenkins-ci/.ssh/known_hosts" -R ${manager_control_public_ip}
        #run_cmd ${manager_control_public_ip} ${VM_MANAGER_USER} ${VM_MANAGER_PASSWD} "${head_cmd} ${scene} ${test_tool} ${protocol} ${test_type} \"${test_length_list}\" > /root/${scene}"
        sshpass -p root ssh -o StrictHostKeyChecking=no root@${manager_control_public_ip} "${cmd}"
        
    done
    return 0
}

function fn_result(){
    local test_scenario_list="Tu-1 Tu-3"
    mkdir ./result
    rm -rf ./result/*
    for scene in ${test_scenario_list}
    do
        #remote_scp_cmd ${manager_control_public_ip} ${VM_MANAGER_USER} ${VM_MANAGER_PASSWD} "/root/${scene}-result.txt" "./result/${scene}" "file"
        sshpass -p root ssh -o StrictHostKeyChecking=no root@${manager_control_public_ip} "cat /root/${scene}-result.txt"
        sshpass -p root scp -o StrictHostKeyChecking=no root@${manager_control_public_ip}:/root/${scene}-result.txt "./result/${scene}"
    done
    return 0
}

function main(){
    fn_parser_ipaddress
    fn_vstf_test_config
    #fn_testing_scenario
    #fn_result
    return 0
}

main
set +x
