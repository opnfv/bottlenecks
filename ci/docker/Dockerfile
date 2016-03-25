##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM ubuntu:14.04
MAINTAINER Qi Liang <liangqi1@huawei.com>

LABEL image=opnfv/bottlenecks

# GIT repo directory
ENV REPOS_DIR /home/opnfv

# Bottlenecks repo
ENV BOTTLENECKS_REPO_DIR ${REPOS_DIR}/bottlenecks
ENV RELENG_REPO_DIR ${REPOS_DIR}/releng

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    sshpass \
    python \
    python-glanceclient \
    python-heatclient \
    python-keystoneclient \
    python-neutronclient \
    python-novaclient

RUN apt-get -y autoremove && \
    apt-get clean

RUN mkdir -p ${REPOS_DIR}

RUN git config --global http.sslVerify false
# TODO fix code clone handler
#RUN git clone https://gerrit.opnfv.org/gerrit/bottlenecks ${BOTTLENECKS_REPO_DIR}
#RUN git clone https://gerrit.opnfv.org/gerrit/releng ${RELENG_REPO_DIR}

