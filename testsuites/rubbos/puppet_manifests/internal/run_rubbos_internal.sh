#!/bin/bash
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


## run_rubbos_interlnal.sh is executed in rubbos-controller
## Usage: run_rubbos_internal.sh rubbos.conf local_result_dir
if [ $# -ne 2 ];then
  echo "Need Two argument!"
  exit 1
fi
local_cfg_path=$1
local_results_dir=$2
controller_host=`hostname`

REMOTE_GIT_REPO=git://git.opnfv.org/bottlenecks
REMOTE_ARTIFACTS_REPO=http://artifacts.opnfv.org/bottlenecks/rubbos/rubbos_files.tar.gz
LOCAL_GIT_REPO=/home/ubuntu/btnks-git
LOCAL_ARTIFACTS_REPO=/home/ubuntu/btnks-artifacts
LOCAL_RUBBOS_MANIFESTS_HOME=/home/ubuntu/btnks-git/bottlenecks/testsuites/rubbos/puppet_manifests
LOCAL_ARTIFACTS_RUBBOS_HOME=/home/ubuntu/btnks-artifacts/rubbos_files

SSH_ARGS="-o StrictHostKeyChecking=no -o BatchMode=yes -i /home/ubuntu/.ssh/id_rsa"

# conf properties from the input config file
client_servers=
web_servers=
app_servers=
cjdbc_controller=
database_servers=
database_port=3306
db_username=rubbos
db_password=rubbos
clients_per_node=
rubbos_app=
rubbos_app_tools=
rubbos_home=

# conf info used in this script
bench_client=
clients_arr=
remote_client_arr=
remote_client_servers=
clients_per_node_arr=
webservers_arr=
appservers_arr=
dbservers_arr=
all_agents_arr=
hostname_arr=
hostip_arr=

# Other variables used in this script
class_nodes=

read_conf() {
  while read line
  do
    if [ ${#line} -gt 0 ] && [ ${line:0:1} != "#" ] && [ ${line:0:1} != "[" ];then
      line=(${line//=/ })
      case ${line[0]} in
        "controller" )
          e_arr=(${line[1]//:/ })
          controller_host=${e_arr[0]}
          controller_ip=${e_arr[2]}
          hostname_arr=("${hostname_arr[@]}" "${e_arr[0]}")
          hostip_arr=("${hostip_arr[@]}" "${e_arr[2]}");;
        "client_servers" )
          elems=(${line[1]//,/ })
          for e in "${elems[@]}";do
            e_arr=(${e//:/ })
            client_servers=${client_servers}${e_arr[0]}","
            hostname_arr=("${hostname_arr[@]}" "${e_arr[0]}")
            hostip_arr=("${hostip_arr[@]}" "${e_arr[1]}")
          done
          client_servers=${client_servers%,};;
        "web_servers" )
          e_arr=(${line[1]//:/ })
          web_servers=${web_servers}${e_arr[0]}","
          hostname_arr=("${hostname_arr[@]}" "${e_arr[0]}")
          hostip_arr=("${hostip_arr[@]}" "${e_arr[1]}")
          web_servers=${e_arr[0]};;
        "app_servers" )
          elems=(${line[1]//,/ })
          for e in "${elems[@]}";do
            e_arr=(${e//:/ })
            app_servers=${app_servers}${e_arr[0]}","
            hostname_arr=("${hostname_arr[@]}" "${e_arr[0]}")
            hostip_arr=("${hostip_arr[@]}" "${e_arr[1]}")
          done
          app_servers=${app_servers%,};;
        "cjdbc_controller" )
          if [ "x"${line[1]} != "x" ]; then
            e_arr=(${line[1]//:/ })
            hostname_arr=("${hostname_arr[@]}" "${e_arr[0]}")
            hostip_arr=("${hostip_arr[@]}" "${e_arr[1]}")
            cjdbc_controller=${e_arr[0]}
          fi
          ;;
        "db_servers" )
          elems=(${line[1]//,/ })
          for e in "${elems[@]}";do
            e_arr=(${e//:/ })
            database_servers=${database_servers}${e_arr[0]}","
            hostname_arr=("${hostname_arr[@]}" "${e_arr[0]}")
            hostip_arr=("${hostip_arr[@]}" "${e_arr[1]}")
          done
          database_servers=${database_servers%,};;
        "database_port" )
          database_port=${line[1]};;
        "db_username" )
          db_username=${line[1]};;
        "db_password" )
          db_password=${line[1]};;
        "clients_per_node" )
          clients_per_node=${line[@]:1:${#line[@]-1}};;
        "rubbos_app" )
          rubbos_app=${line[1]};;
        "rubbos_app_tools" )
          rubbos_app_tools=${line[1]};;
        "rubbos_home" )
          rubbos_home=${line[1]};;
      esac
    fi
  done < $local_cfg_path

  clients_arr=(${client_servers//,/ })
  clients_per_node_arr=(${clients_per_node})
  webservers_arr=(${web_servers//,/ })
  appservers_arr=(${app_servers//,/ })
  dbservers_arr=(${database_servers//,/ })
  all_agents_arr=("${clients_arr[@]}" "${webservers_arr[@]}" "${appservers_arr[@]}" "${dbservers_arr[@]}")
  bench_client=${clients_arr[0]}
  len=${#clients_arr[@]}
  if [ $len -gt 1 ]; then
    remote_clients_arr=(${clients_arr[@]:1:$len-1})
    remote_client_servers=${client_servers#*,}
  fi

  echo "-------------Main conf info:----------"
  i=1
  while [ $i -lt ${#hostname_arr[@]} ]; do
    echo ${hostip_arr[$i]}" "${hostname_arr[$i]}
    let i=i+1
  done
  echo "clients_arr:           "${clients_arr[@]}
  echo "bench_client:          "$bench_client
  echo "remote_client_servers: "$remote_client_servers
  echo "remote_clients_arr:    "${remote_clients_arr[@]}
  echo "clients_per_node_arr:  "${clients_per_node_arr[@]}
  echo "webservers_arr:        "${webservers_arr[@]}
  echo "appservers_arr:        "${appservers_arr[@]}
  echo "dbservers_arr:         "${dbservers_arr[@]}
  echo "all agents:            "${all_agents_arr[@]}
}

fetch_remote_resources() {
  if [ -d $LOCAL_GIT_REPO ];then
    rm -rf $LOCAL_GIT_REPO
  fi
  mkdir -p $LOCAL_GIT_REPO
  sudo apt-get install -y git
  cd $LOCAL_GIT_REPO
  git clone ${REMOTE_GIT_REPO}

  if [ -d $LOCAL_ARTIFACTS_REPO ];then
    rm -rf $LOCAL_ARTIFACTS_REPO
  fi
  mkdir -p $LOCAL_ARTIFACTS_REPO
  cd $LOCAL_ARTIFACTS_REPO
  wget -nv ${REMOTE_ARTIFACTS_REPO}
  tar xvzf rubbos_files.tar.gz

  if [ -d $local_results_dir ];then
    rm -rf $local_results_dir
  fi
  mkdir -p $local_results_dir
}

# ssh all vms/instances once only after first creation
direct_ssh() {
  echo "127.0.0.1 $(hostname)" >> /etc/hosts
  echo "write hosts file: 127.0.0.1 $(hostname)"
  cp ${LOCAL_GIT_REPO}/bottlenecks/utils/infra_setup/bottlenecks_key/bottlenecks_key /home/ubuntu/.ssh/id_rsa
  sudo chmod 0600 /home/ubuntu/.ssh/id_rsa
  echo 'StrictHostKeyChecking no' > /home/ubuntu/.ssh/config
  sudo chown -R ubuntu:ubuntu /home/ubuntu/.ssh
  i=1
  while [ $i -lt ${#hostip_arr[@]} ]; do
    echo ${hostip_arr[$i]}" "${hostname_arr[$i]} >> /etc/hosts
    let i=i+1
  done
  echo "Done controller."

  i=1
  while [ $i -lt ${#hostip_arr[@]} ]; do
    if [ ${hostname_arr[$i]} == ${controller_host} ];then
      let i=i+1
      continue
    fi
    echo "Processing: "${hostip_arr[$i]}" "${hostname_arr[$i]}
    echo "ssh *sudo hostname* test:"
    ssh ${SSH_ARGS} ubuntu@${hostip_arr[$i]} "sudo hostname"

    ssh ${SSH_ARGS} ubuntu@${hostip_arr[$i]} "sudo cp /etc/hosts /home/ubuntu/ && sudo chmod 646 /home/ubuntu/hosts"
    ssh ${SSH_ARGS} ubuntu@${hostip_arr[$i]} "echo 127.0.0.1 ${hostname_arr[$i]} >> /home/ubuntu/hosts"
    j=1
    while [ $j -lt ${#hostip_arr[@]} ];do
      local host_item=${hostip_arr[$j]}" "${hostname_arr[$j]}
      ssh ${SSH_ARGS} ubuntu@${hostip_arr[$i]} "echo ${host_item} >> /home/ubuntu/hosts"
      let j=j+1
    done
    ssh ${SSH_ARGS} ubuntu@${hostip_arr[$i]} "sudo chmod 644 /home/ubuntu/hosts && sudo cp /home/ubuntu/hosts /etc/ && sudo rm -rf /home/ubuntu/hosts"
    echo "done hosts"

    sudo ssh ${SSH_ARGS} ubuntu@${hostip_arr[$i]} "echo 'StrictHostKeyChecking no' > /home/ubuntu/.ssh/config"
    sudo scp ${SSH_ARGS} /home/ubuntu/.ssh/id_rsa ubuntu@${hostip_arr[$i]}:/home/ubuntu/.ssh/

    let i=i+1
  done
}

start_puppet_service() {
  # Start puppetserver
  sudo service puppetserver stop
  sudo service puppetserver start
  sudo service puppetserver status
  # Start all puppet agents
  for host in "${all_agents_arr[@]}";do
    echo "start puppet agent on:"${host}
    ssh ${SSH_ARGS} ubuntu@${host} "sudo service puppet status"
    ssh ${SSH_ARGS} ubuntu@${host} "sudo service puppet stop"
    ssh ${SSH_ARGS} ubuntu@${host} "sudo service puppet start --no-client"
    ssh ${SSH_ARGS} ubuntu@${host} "sudo service puppet status"
  done

  sudo puppet cert list --all
  sudo puppet cert sign --all
  sudo puppet cert list --all
}

# inline function
# It requires one local file path which needs to be replaced
_replace_text() {
  echo "_replace file: "$1
  sed -i 's#REPLACED_RUBBOS_APP_TOOLS#'${rubbos_app_tools}'#g' $1
  sed -i 's#REPLACED_RUBBOS_APP#'${rubbos_app}'#g' $1
  sed -i 's#REPLACED_RUBBOS_HOME#'${rubbos_home}'#g' $1
  local mysql_jdbc_url="jdbc:mysql://"${database_servers}":"${database_port}"/rubbos"
  sed -i 's#REPLACED_MYSQL_JDBC_DB_URL#'${mysql_jdbc_url}'#g' $1
  sed -i 's/REPLACED_MYSQL_USERNAME/'${db_username}'/g' $1
  sed -i 's/REPLACED_MYSQL_PASSWORD/'${db_password}'/g' $1
  handler_details=
  handlers=
  i=0
  while [ $i -lt ${#appservers_arr} ];do
    handler_name="s"$i
    handlers=${handlers}${handler_name}","
    handler_details=${handler_details}"worker."${handler_name}".port=8009\n"
    handler_details=${handler_details}"worker."${handler_name}".host="${appservers_arr[$i]}"\n"
    handler_details=${handler_details}"worker."${handler_name}".type=ajp13\n"
    handler_details=${handler_details}"worker."${handler_name}".lbfactor=1\n"
    let i=i+1
  done
  handlers=${handlers%,}
  sed -i 's/REPLACED_HANDLERS_DETAILS/'${handler_details}'/g' $1
  sed -i 's/REPLACED_HANDLERS/'${handlers}'/g' $1

  sed -i 's/REPLACED_WEB_SERVER/'${web_servers}'/g' $1
  sed -i 's/REPLACED_APPLICATION_SERVER/'${app_servers}'/g' $1
  sed -i 's/REPLACED_DB_SERVER/'${database_servers}'/g' $1
  sed -i 's/REPLACED_CLIENT_SERVERS/'${remote_client_servers}'/g' $1
}

# inline function
# it requires one input string
_to_puppet_class_nodes() {
  echo "_to_puppet_class_nodes "$1
  class_nodes=
  nodes_arr=(${1//,/ })
  i=0
  while [ $i -lt ${#nodes_arr[@]} ];do
    class_nodes=${class_nodes}"'"${nodes_arr[$i]}"',"
    let i=i+1
  done
  class_nodes=${class_nodes%,}
}

# inline function
_execute_catalog() {
  for host in "${clients_arr[@]}"; do
    ssh ${SSH_ARGS} ubuntu@${host} 'sudo puppet agent -t' &
  done
  for host in "${webservers_arr[@]}"; do
    ssh ${SSH_ARGS} ubuntu@${host} 'sudo puppet agent -t'
  done
  for host in "${appservers_arr[@]}"; do
    ssh ${SSH_ARGS} ubuntu@${host} 'sudo puppet agent -t'
  done
  for host in "${dbservers_arr[@]}"; do
    ssh ${SSH_ARGS} ubuntu@${host} 'sudo puppet agent -t'
  done
}

prepare_manifests() {
  # copy manifests
  sudo cp -r ${LOCAL_RUBBOS_MANIFESTS_HOME}/modules/* /etc/puppet/modules/

  # copy rubbos_files
  sudo cp -r ${LOCAL_ARTIFACTS_RUBBOS_HOME}/modules/* /etc/puppet/modules/

  # adjust corresponding configuration files (pre-catalog)
  _replace_text /etc/puppet/modules/rubbos_tomcat/files/tomcat_sl/build.properties
  _replace_text /etc/puppet/modules/rubbos_tomcat/files/tomcat_sl/Config.java
  _replace_text /etc/puppet/modules/rubbos_tomcat/files/tomcat_sl/mysql.properties
  _replace_text /etc/puppet/modules/rubbos_httpd/files/apache_conf/workers.properties
  _replace_text /etc/puppet/modules/rubbos_httpd/files/apache_conf/httpd.conf
  _replace_text /etc/puppet/modules/rubbos_client/files/build.properties
  _replace_text /etc/puppet/modules/rubbos_client/files/rubbos.properties.template
  _replace_text /etc/puppet/modules/rubbos_client/files/run_emulator.sh
}

execute_catalog() {
  # start all (exec catalog)
  if [ "x"$1 == "xstart" ];then
    echo "--> Start to execute catalogs in all agents..."
    sudo cp ${LOCAL_RUBBOS_MANIFESTS_HOME}/site_on.pp /etc/puppet/manifests/site.pp
    _execute_catalog
    echo "--> Finish to execute catalogs in all agents."
  elif [ "x"$1 == "xclean" ];then
    echo "--> Cleanup all agents..."
    sudo cp ${LOCAL_RUBBOS_MANIFESTS_HOME}/site_off.pp /etc/puppet/manifests/site.pp
    _execute_catalog
   echo "--> Finish to cleanup all agents."
  fi
}

run_emulator() {
  # prepare data in db servers
  for host in "${dbservers_arr[@]}"; do
    ssh ${SSH_ARGS} ubuntu@${host} 'sudo scp ubuntu@'${controller_host}':/etc/puppet/modules/rubbos_mysql/files/rubbos_data_sql.tar.gz '${rubbos_home}''
    ssh ${SSH_ARGS} ubuntu@${host} 'cd '${rubbos_home}' && sudo ./prepare_rubbos_mysql_db.sh ./rubbos_data_sql.tar.gz ./rubbos_data_sql_dir'
  done

  # run emulator.sh ( Modify rubbos.properties file first)
  ssh ${SSH_ARGS} ubuntu@${bench_client} 'sudo rm -rf '${rubbos_home}'/bench/bench'
  for x in "${clients_per_node_arr[@]}";do
    echo "run emulator with clients_per_node="$x
    for host in "${clients_arr[@]}";do
      ssh ${SSH_ARGS} ubuntu@${host} "sed -e 's/REPLACED_NUMBER_OF_CLIENTS_PER_NODE/'${x}'/g' '${rubbos_home}'/Client/rubbos.properties.template > '${rubbos_home}'/Client/rubbos.properties "
    done
    ssh ${SSH_ARGS} ubuntu@${bench_client} 'cd '${rubbos_home}'/bench && ./run_emulator.sh'
  done
}

collect_results() {
  # collect results, from bench_host to controller
  scp ${SSH_ARGS} -r ubuntu@${bench_client}:${rubbos_home}/bench/bench/* ${local_results_dir}
}

process_results() {
  # post-process results and push to the database of dashboard
  python ${LOCAL_GIT_REPO}/bottlenecks/utils/dashboard/process_data.py -i ${local_results_dir} \
        -c ${LOCAL_GIT_REPO}/bottlenecks/utils/dashboard/dashboard.yaml \
        -s rubbos \
        -o ${local_results_dir}/rubbos.out \
        -u no
}

main() {
  echo "==> read_conf:"
  read_conf
  echo "==> fetch_remote_resources:"
  fetch_remote_resources
  echo "==> direct_ssh:"
  direct_ssh
  echo "==> start_puppet_service:"
  start_puppet_service
  echo "==> prepare_manifests:"
  prepare_manifests
  echo "==> execute_catalog start:"
  execute_catalog start
  echo "==> run_emulator:"
  run_emulator
  echo "==> collect_results (to controller:${local_results_dir}):"
  collect_results
  echo "==> process_results:"
  process_results
  echo "==> execute_catalog clean:"
  execute_catalog clean
}

main
