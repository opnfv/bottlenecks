#!/bin/bash
##############################################################################
# Copyright (c) 2017 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
MONITOR_CONFIG="/home/opnfv/bottlenecks/monitor/config"
DISPATCH="/home/opnfv/bottlenecks/monitor/dispatch"
OPENSTACK_ENV=${MONITOR_CONFIG}/openstack_exporter.conf

usage="Script to run the tests in Bottlenecks.

usage:
    bash $(basename "$0") [-h|--help] [-i|--installer <installer typer>] [-o|--openstack-env <openstack env>]

where:
    -h|--help         show the help text
    -i|--installer    specify the installer for the system to be monitored
      <installer type>
                      one of the following:
                              (apex, compass)
    -o|--opentack-env specify the openstack env file for openstack monitoring
                      defalt value is \"${MONITOR_CONFIG}/openstack_exporter.conf\"

examples:
    $(basename "$0") -i compass"


info () {
    logger -s -t "BOTTLENECKS INFO" "$*"
}

error () {
    logger -s -t "BOTTLENECKS ERROR" "$*"
    exit 1
}

# Process input variables
while [[ $# > 0 ]]
    do
    key="$1"
    case $key in
        -h|--help)
            echo "$usage"
            exit 0
            shift
        ;;
        -i|--installer)
            INSTALLER_TYPE="$2"
            shift
        ;;
        -o|--openstack-env)
            OPENSTACK_ENV="$2"
            shift
        ;;
        *)
            error "unkown input options $1 $2"
            exit 1
        ;;
     esac
     shift
done


barometer_client_install_sh="/home/opnfv/bottlenecks/monitor/dispatch/install_barometer_client.sh"
barometer_client_install_conf="/home/opnfv/bottlenecks/monitor/config/barometer_client.conf"

cadvisor_client_install_sh="/home/opnfv/bottlenecks/monitor/dispatch/install_cadvisor_client.sh"

collectd_client_install_sh="/home/opnfv/bottlenecks/monitor/dispatch/install_collectd_client.sh"
collectd_client_install_conf="/home/opnfv/bottlenecks/monitor/config/collectd_client.conf"

# INSTALL GRAFANA + PROMETHEUS + CADVISOR + BAROMETER on the JUMPERSERVER
# # Node-Exporter
echo == installation of monitoring module is started ==

# # Collectd
# # Configure IP Address in collectd server configuration
# python ${DISPATCH}/server_ip_configure.py ${MONITOR_CONFIG}/collectd_server.conf
# sudo docker run --name bottlenecks-collectd -d \
#   --privileged \
#   -v ${MONITOR_CONFIG}/collectd_server.conf:/etc/collectd/collectd.conf:ro \
#   -v /proc:/mnt/proc:ro \
#   fr3nd/collectd:5.5.0-1

set +e
# Prometheus
sudo docker run --name bottlenecks-prometheus \
  -d -p 9090:9090 \
  -v ${MONITOR_CONFIG}/prometheus.yaml:/etc/prometheus/prometheus.yml \
  prom/prometheus:v1.7.1

# Collectd-Exporter
sudo docker run --name bottlenecks-collectd-exporter \
  -d -p 9103:9103 -p 25826:25826/udp \
  prom/collectd-exporter:0.3.1 \
  -collectd.listen-address=":25826"

sudo docker run --name bottlenecks-node-exporter \
  -d -p 9100:9100 \
  -v "/proc:/host/proc:ro" \
  -v "/sys:/host/sys:ro" \
  -v "/:/rootfs:ro" \
  quay.io/prometheus/node-exporter:v0.14.0 \
    -collector.procfs /host/proc \
    -collector.sysfs /host/sys \
    -collector.filesystem.ignored-mount-points "^/(sys|proc|dev|host|etc)($|/)"

# Openstack-Exporter
sudo docker run --name bottlenecks-openstack-exporter \
  -v /tmp:/tmp \
  -p 9104:9104 --env-file ${OPENSTACK_ENV} \
  -d gabrielyuyang/openstack-exporter:1.0

# Grafana
sudo  docker run --name bottlenecks-grafana \
  -d -p 3000:3000 \
  -v ${MONITOR_CONFIG}/grafana.ini:/etc/grafana/grafana.ini \
  grafana/grafana:4.5.0
# Automate Prometheus Datasource and Grafana Dashboard creation

set -e
sleep 5
python ${DISPATCH}/../dashboard/automated_dashboard_datasource.py

set +e
# Cadvisor
sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=bottlenecks-cadvisor \
  google/cadvisor:v0.25.0


set -e
# Barometer
# Configure IP Address in barometer server configuration
sleep 5
python ${DISPATCH}/server_ip_configure.py ${MONITOR_CONFIG}/barometer_server.conf

set +e
# Install on jumpserver
docker pull opnfv/barometer
sudo docker run  --name bottlenecks-barometer -d --net=host \
  -v ${MONITOR_CONFIG}/barometer_server.conf:/src/barometer/src/collectd/collectd/src/collectd.conf \
  -v ${MONITOR_CONFIG}/barometer_server.conf:/opt/collectd/etc/collectd.conf \
  -v /var/run:/var/run \
  -v /tmp:/tmp \
  --privileged opnfv/barometer /run_collectd.sh

set -e
# INSTALL BAROMETER + CADVISOR (+ COLLECTD) CLIENTS on COMPUTE/CONTROL NODES
# Configure IP Address in barometer client configuration
python ${DISPATCH}/client_ip_configure.py ${MONITOR_CONFIG}/barometer_client.conf

# Automate Barometer client installation
python ${DISPATCH}/install_clients.py \
  -i ${INSTALLER_TYPE} -s ${barometer_client_install_sh} \
  -c ${barometer_client_install_conf}

# # Configure IP Address in collectd client configuration
# python ${DISPATCH}/client_ip_configure.py ${MONITOR_CONFIG}/collectd_client.conf
# # Automate Collectd Client installation
# python ${DISPATCH}/automate_collectd_client.py

# Automate Cadvisor Client
python ${DISPATCH}/install_clients.py \
  -i ${INSTALLER_TYPE} -s ${cadvisor_client_install_sh}

echo == installation of monitoring module is finished ==
