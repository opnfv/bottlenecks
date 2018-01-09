#!/bin/bash
##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
if grep -q "cadvisor" /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
then
    sed -e "/cadvisor-port=0/d" -i /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
    systemctl daemon-reload
    systemctl restart kubelet
    
    git clone https://github.com/coreos/prometheus-operator.git
    cd prometheus-operator
    
    kubectl apply -n kube-system -f bundle.yaml
    
    cd contrib/kube-prometheus
    sleep 10
    hack/cluster-monitoring/deploy
fi
