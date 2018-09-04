##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

group="x-lab"
# ui image name
ui_image="$group/test-scheduler:ui"
# ui container name
ui_container="t-scheduler-ui"
docker rm -f $ui_container
docker rmi $ui_image
# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)
rm -rf $basepath/dist
