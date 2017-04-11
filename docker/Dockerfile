##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM ubuntu:14.04
MAINTAINER MatthewLi <matthew.lijun@huawei.com>

LABEL image=opnfv/bottlenecks

# GIT repo directory
ENV REPOS_DIR /home/opnfv

# CI docker image label
ARG BRANCH=master

# Bottlenecks repo
ENV BOTTLENECKS_REPO_DIR ${REPOS_DIR}/bottlenecks
ENV RELENG_REPO_DIR ${REPOS_DIR}/releng
ENV creds ${BOTTLENECKS_REPO_DIR}/config/openstack.creds

#new test suite required packages can be added here
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    curl \
    wget \
    git \
    sshpass \
    python \
    python-dev \
    python-pip \
    vim \
    python-setuptools && \
    easy_install -U setuptools==30.0.0

RUN apt-get -y autoremove && \
    apt-get clean

RUN mkdir -p ${REPOS_DIR}

RUN git config --global http.sslVerify false
RUN git clone -b $BRANCH https://gerrit.opnfv.org/gerrit/bottlenecks ${BOTTLENECKS_REPO_DIR}
RUN git clone https://gerrit.opnfv.org/gerrit/releng ${RELENG_REPO_DIR}

RUN easy_install pytz
RUN pip install -r ${REPOS_DIR}/bottlenecks/requirements/requirements.txt
RUN pip install -U /home/opnfv/bottlenecks
