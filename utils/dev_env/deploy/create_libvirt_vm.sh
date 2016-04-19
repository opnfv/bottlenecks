#!/bin/bash
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


##############################################
#  Usage: ./deploy.sh paras_conf outout_dir
##############################################
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
tool_dir=${0%/*}

function print_usage()
{
    echo "Usage: ./deploy.sh paras_conf output_dir"
}

## sanity check
if [ ! -f $tool_dir/mac_generator.sh ] || \
    [ ! -f $tool_dir/libvirt_template.xml ] || \
    [ ! -f $tool_dir/meta-data.template ] || \
    [ ! -f $tool_dir/user-data.template ] || \
    [ ! -f $tool_dir/p-master-user-data.template ] || \
    [ ! -f $tool_dir/p-agent-user-data.template ]; then
      echo "Lack some necessary files for this tool!"
      echo "deploy.sh"
      echo "mac_generator.sh"
      echo "1 xml, and 4 template"
      exit 1
fi

## Check input
if [ $# != 2 ]; then
    print_usage
    exit 1
fi
if [ ! -f $1 ]; then
    echo "Cannot find file: "$1
    exit 1
fi
if [ -d $2 ]; then
    echo "Ouput dir $2 exist!"
    exit 1
fi

## Assign parameters
host_names=""
puppet_enable="true"
master_host=""
vm_mem=
vm_cpu_cores=
image_url=
image_name=
ipaddr_start=
trusted_ssh_pub_keys_file=
while read line
do
    line=(${line//=/ })
    case ${line[0]} in
        "host_names" )
            host_names=${line[1]}
        ;;
        "puppet_enable" )
            puppet_enable=${line[1]}
        ;;
        "master_host" )
            master_host=${line[1]}
        ;;
        "vm_mem" )
            vm_mem=${line[1]}
        ;;
        "vm_cpu_cores" )
            vm_cpu_cores=${line[1]}
        ;;
        "image_url" )
            image_url=${line[1]}
        ;;
        "image_name" )
            image_name=${line[1]}
        ;;
        "ipaddr_start" )
            ipaddr_start=${line[1]}
        ;;
        "trusted_ssh_pub_keys_file" )
            trusted_ssh_pub_keys_file=${line[1]}
        ;;
    esac
done < $1

echo "puppet_enable="$puppet_enable

# Check parameters in conf file
if [ $puppet_enable == "true" ] ; then
    if [ ${#master_host} == 0 ];then
        echo "Should specify master_host!"
        exit 1
    else
        result=$(echo ${host_names} | grep  "${master_host}")
        if [ ${result} == "" ]; then
            echo "Specified master_host is invalid!"
            exit 1
        fi
    fi
fi

# Define and Prepare needed data
mac_arr=
hostname_arr=(${host_names//,/ })
virt_num=${#hostname_arr[@]}
ip_arr=()
replaced_hosts=""
replaced_ssh_keys=""
output_dir=$2
work_dir=
host_vm_dir=
cache_dir=
function init(){
    # Generate mac address
    local mac_generator=${tool_dir}/mac_generator.sh
    chmod +x $mac_generator
    mac_str=$($mac_generator $virt_num)
    mac_arr=($mac_str)

    # Generate hosts info
    local ip=""
    i=0
    for host in "${hostname_arr[@]}"; do
        ip=${ipaddr_prefix}$((i+$ipaddr_idx))
        ip_arr+=($ip)
        # Note the format, especially the space
        replaced_hosts=${replaced_hosts}"      "${ip}" "${host}"\n"
        let i=i+1
    done

    # Generate ssh public keys
    echo "## trusted_ssh_pub_keys_file --> "${trusted_ssh_pub_keys_file}
    if [ ${trusted_ssh_pub_keys_file} != "" ] && [ -f ${trusted_ssh_pub_keys_file} ]; then
        while read line
        do
            # Note the format, especially space
            replaced_ssh_keys=${replaced_ssh_keys}"    - "${line}"\n"
        done < ${trusted_ssh_pub_keys_file}
        # delete last "\n" in replaced_ssh_keysi
        replaced_ssh_keys=${replaced_ssh_keys%\\n}
    fi

    # Prepare needed folder and files
    if [ ${output_dir:0-1} == "/" ]; then
        output_dir=${output_dir%/*}
    fi
    output_file=$output_dir/hosts.info
    mkdir -p $output_dir
    touch $output_file
    echo "## Output host_info file --> "$output_file

    work_dir=$output_dir/work
    host_vm_dir=$work_dir/vm
    cache_dir=$work_dir/cache
    mkdir -p $work_dir
    mkdir -p $host_vm_dir
    mkdir -p $cache_dir

    # Cache img file
    echo "## Cache img file"
    curl --connect-timeout 10 -o ${cache_dir}/$image_name $image_url
}

# Bring up instances/vms
sub_ip_arr=(${ipaddr_start//./ })
ipaddr_prefix=${sub_ip_arr[0]}"."${sub_ip_arr[1]}"."${sub_ip_arr[2]}"."
ipaddr_idx=${sub_ip_arr[3]}
function bring_up() {
    i=0
    while (($i < $virt_num))
    do
        echo "Bring up a vm, hostname: ${hostname_arr[$i]}, ip: ${ip_arr[$i]}, mac: ${mac_arr[$i]}"
        vm_dir=$host_vm_dir/${hostname_arr[$i]}
        mkdir -p $vm_dir
        cp ${cache_dir}/$image_name $vm_dir

        sed -e "s/REPLACE_IPADDR/${ip_arr[$i]}/g" \
            -e "s/REPLACE_GATEWAY/${ipaddr_prefix}1/g" \
            -e "s/REPLACE_HOSTNAME/${hostname_arr[$i]}/g" \
            ${tool_dir}/meta-data.template > ${cache_dir}/meta-data

        if [ ${puppet_enable} == "true" ]; then
            # Use puppet user data
            echo "hostname: "${hostname_arr[$i]}
            if [ ${hostname_arr[$i]} == ${master_host} ]; then
                cp ${tool_dir}/p-master-user-data.template ${cache_dir}/user-data.template
            else
                cp ${tool_dir}/p-agent-user-data.template ${cache_dir}/user-data.templatate
            fi
            sed -e "s#REPLACED_TRUSTED_PUB_SSH_KEYS#${replaced_ssh_keys}#g" \
                -e "s#REPLACED_HOSTS_INFO#${replaced_hosts}#g" \
                -e "s/REPLACED_PUPPET_MASTER_SERVER/${master_host}/g" \
                ${cache_dir}/user-data.template > ${cache_dir}/user-data
        else
           # Use common user data
           echo "## Use common user-data.template"
           cp ${tool_dir}/user-data.template ${cache_dir}/user-data
        fi

        genisoimage -output seed.iso -volid cidata -joliet -rock ${cache_dir}/user-data ${cache_dir}/meta-data
        mv seed.iso ${vm_dir}/
        # Create vm xml
        sed -e "s/REPLACE_MEM/$vm_mem/g" \
            -e "s/REPLACE_CPU/$vm_cpu_cores/g" \
            -e "s/REPLACE_NAME/${hostname_arr[$i]}/g" \
            -e "s#REPLACE_IMAGE#$vm_dir/disk.img#g" \
            -e "s#REPLACE_SEED_IMAGE#$vm_dir/seed.iso#g" \
            -e "s/REPLACE_MAC_ADDR/${mac_arr[$i]}/g" \
            ${tool_dir}/libvirt_template.xml > ${vm_dir}/libvirt.xml

        echo "${ip_arr[$i]} ${hostname_arr[$i]}" >> $output_file

        echo "Will define xml from:"${vm_dir}"/libvirt.xml"
        echo "start: "${hostname_arr[$i]}
        sudo virsh define ${vm_dir}/libvirt.xml
        sudo virsh start ${hostname_arr[$i]}
        let i=i+1
        rm -rf ${cache_dir}/meta-data ${cache_dir}/user-data
    done
}

function clean(){
    rm -rf ${cache_dir}
}

init
bring_up
clean
