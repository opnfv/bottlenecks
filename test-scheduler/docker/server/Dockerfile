##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM python:2.7
MAINTAINER x-lab/Leo
WORKDIR /home/test-scheduler/server
COPY ./server .

RUN pip install -r ./python_modules.txt

ENV CONDUCTOR_DIR /home/test-scheduler/conductor
RUN mkdir ${CONDUCTOR_DIR} && cd ${CONDUCTOR_DIR} && \
    git clone http://github.com/Netflix/conductor.git && \
    cd conductor && git checkout v1.10.4
RUN cd ${CONDUCTOR_DIR}/conductor/client/python && \
    python setup.py install

RUN pip install -U .

EXPOSE 5310
EXPOSE 5312
CMD sh -c 'python /usr/local/lib/python2.7/site-packages/src/rest/router.py &  \
           python ./src/rest/test_service_demo.py'
