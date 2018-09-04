##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM node:alpine
MAINTAINER x-lab/Leo
WORKDIR /home/test-scheduler/ui
COPY ./ui .

RUN npm install
RUN npm run build

CMD tail -f /dev/null
