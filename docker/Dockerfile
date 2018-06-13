##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM ubuntu:16.04
MAINTAINER Yang (Gabriel) Yu <gabriel.yuyang@huawei.com>

LABEL image=opnfv/bottlenecks

# GIT repo directory
ENV REPOS_DIR /home/opnfv

# CI docker image label
ARG BRANCH=master

# Bottlenecks repo
ENV BOTTLENECKS_REPO_DIR ${REPOS_DIR}/bottlenecks
ENV RELENG_REPO_DIR ${REPOS_DIR}/releng

#new test suite required packages can be added here
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    python \
    python-pip \
    vim \
    iputils-ping \
    python-setuptools && \
    apt-get -y autoremove && \
    apt-get clean  

RUN easy_install -U setuptools==30.0.0

RUN mkdir -p ${REPOS_DIR}

RUN git config --global http.sslVerify false
RUN git clone -b $BRANCH https://gerrit.opnfv.org/gerrit/bottlenecks ${BOTTLENECKS_REPO_DIR}
RUN git clone https://gerrit.opnfv.org/gerrit/releng ${RELENG_REPO_DIR}

RUN pip install -r ${BOTTLENECKS_REPO_DIR}/requirements/requirements.txt
RUN pip install -U ${BOTTLENECKS_REPO_DIR}
