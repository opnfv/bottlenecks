##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM nginx
MAINTAINER x-lab/Leo

RUN rm /etc/nginx/conf.d/default.conf

ADD ./ui/config/default.conf /etc/nginx/conf.d/
COPY ./docker/ui/dist/  /usr/share/nginx/html/
