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
GRAFANA="/home/opnfv/bottlenecks/monitor/grafana"

# Node-Exporter
sudo docker run --name bottlenecks-node-exporter \
  -d -p 9100:9100 \
  -v "/proc:/host/proc:ro" \
  -v "/sys:/host/sys:ro" \
  -v "/:/rootfs:ro" \
  --net="host" \
  quay.io/prometheus/node-exporter:v0.14.0 \
    -collector.procfs /host/proc \
    -collector.sysfs /host/sys \
    -collector.filesystem.ignored-mount-points "^/(sys|proc|dev|host|etc)($|/)"

# Collectd
sudo docker run --name bottlenecks-collectd -d \
  --privileged \
  -v ${MONITOR_CONFIG}:/etc/collectd:ro \
  -v /proc:/mnt/proc:ro \
  fr3nd/collectd:5.5.0-1

# Collectd-Exporter
sudo docker run --name bottlenecks-collectd-exporter \
  -d -p 9103:9103 \
  -p 25826:25826/udp prom/collectd-exporter:0.3.1 \
  -collectd.listen-address=":25826"

# Prometheus
sudo docker run --name bottlenecks-prometheus \
  -d -p 9090:9090 \
  -v ${MONITOR_CONFIG}/prometheus.yaml:/etc/prometheus/prometheus.yml \
  prom/prometheus:v1.7.1

# Grafana
sudo  docker run --name bottlenecks-grafana \
  -d -p 3000:3000 \
  -v ${GRAFANA}/config/grafana.ini:/etc/grafana/grafana.ini \
  grafana/grafana:4.5.0

# Cadvisor
sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  google/cadvisor:v0.25.0 \ -storage_driver=Prometheus

# Automate Collectd Client
python automate_collectd_client.py

# Automate Cadvisor Client
python automate_cadvisor_client.py

# Automate Prometheus Datasource and Grafana Dashboard creation
python automated-dashboard-datasource.py
