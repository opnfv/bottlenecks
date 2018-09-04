##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

conductor_network='conductor_default'
group="x-lab"
# server image name
server_image="$group/test-scheduler:server"
# server container name
server_container="t-scheduler-server"

docker run -d --rm -p 5310:5310 -p 5312:5312 --net=$conductor_network --name $server_container $server_image
