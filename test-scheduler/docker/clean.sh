##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

sudo docker rm -f t-scheduler-server \
                  t-scheduler-ui \
                  conductor_conductor-server_1 \
                  conductor_conductor-ui_1 \
                  conductor_dynomite_1 \
                  conductor_elasticsearch_1

sudo docker network rm conductor_default

sudo docker rmi x-lab/test-scheduler:server \
                x-lab/test-scheduler:ui \
                x-lab/conductor:builder \
                conductor:ui \
                conductor:server \
                elasticsearch:2.4 \
                v1r3n/dynomite:latest \
                java:8-jre-alpine \
                python:2.7 \
                node:alpine \
                nginx:latest \
                java:latest \

echo "--- Clean Finished ---"
