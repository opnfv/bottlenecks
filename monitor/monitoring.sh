#!/bin/bash
##############################################################################
# Copyright (c) 2017 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -e

MONITOR_CONFIG="/home/opnfv/bottlenecks/monitor/config"
DISPATCH="/home/opnfv/bottlenecks/monitor/dispatch"


# INSTALL GRAFANA + PROMETHEUS + CADVISOR + BAROMETER on the JUMPERSERVER
# # Node-Exporter
# sudo docker run --name bottlenecks-node-exporter \
#   -d -p 9100:9100 \
#   -v "/proc:/host/proc:ro" \
#   -v "/sys:/host/sys:ro" \
#   -v "/:/rootfs:ro" \
#   --net="host" \
#   quay.io/prometheus/node-exporter:v0.14.0 \
#     -collector.procfs /host/proc \
#     -collector.sysfs /host/sys \
#     -collector.filesystem.ignored-mount-points "^/(sys|proc|dev|host|etc)($|/)"

# # Collectd
# # Configure IP Address in collectd server configuration
# python ${DISPATCH}/server_ip_configure.py ${MONITOR_CONFIG}/collectd_server.conf
# sudo docker run --name bottlenecks-collectd -d \
#   --privileged \
#   -v ${MONITOR_CONFIG}/collectd_server.conf:/etc/collectd/collectd.conf:ro \
#   -v /proc:/mnt/proc:ro \
#   fr3nd/collectd:5.5.0-1

echo == installation of monitoring module is started ==

set +e
# Collectd-Exporter
sudo docker run --name bottlenecks-collectd-exporter \
  -d -p 9103:9103 -p 25826:25826/udp \
  prom/collectd-exporter:0.3.1 \
  -collectd.listen-address=":25826"

# Prometheus
sudo docker run --name bottlenecks-prometheus \
  -d -p 9090:9090 \
  -v ${MONITOR_CONFIG}/prometheus.yaml:/etc/prometheus/prometheus.yml \
  prom/prometheus:v1.7.1

# Grafana
sudo  docker run --name bottlenecks-grafana \
  -d -p 3000:3000 \
  -v ${MONITOR_CONFIG}/grafana.ini:/etc/grafana/grafana.ini \
  grafana/grafana:4.5.0
# Automate Prometheus Datasource and Grafana Dashboard creation

set -e
python dashboard/automated_dashboard_datasource.py

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
sleep 10
python ${DISPATCH}/server_ip_configure.py ${MONITOR_CONFIG}/barometer_server.conf

set +e
# Install on jumpserver
docker pull opnfv/barometer
sudo docker run  --name bottlenecks-barometer -tid --net=host \
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
python ${DISPATCH}/automate_barometer_client.py

# # Configure IP Address in collectd client configuration
# python ${DISPATCH}/client_ip_configure.py ${MONITOR_CONFIG}/collectd_client.conf
# # Automate Collectd Client installation
# python ${DISPATCH}/automate_collectd_client.py

# Automate Cadvisor Client
python ${DISPATCH}/automate_cadvisor_client.py

echo == installation of monitoring module is finished ==
