##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM java
MAINTAINER x-lab/Leo
RUN useradd -m noroot -s /bin/bash
USER noroot
WORKDIR /home/noroot
ENV BUILD_DIR build_dir
ENV REPO_DIR ${BUILD_DIR}/conductor

RUN mkdir -p ${BUILD_DIR} && cd ${BUILD_DIR} && \
    git clone http://github.com/Netflix/conductor.git && \
    cd conductor && git checkout v1.10.4

RUN cd ${REPO_DIR} && ./gradlew build

CMD tail -f /dev/null
