##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)
tmppath=$basepath/tmp_files
docker_tmppath=/home/noroot/build_dir/conductor
group="x-lab"
plugin_image="$group/conductor:builder"
plugin_container="conductor-builder"
#build the gradle project in a temp container.

mkdir -p $tmppath
docker build -t $plugin_image -f $basepath/Dockerfile $basepath
docker run -d --name $plugin_container $plugin_image
docker cp  $plugin_container:$docker_tmppath $tmppath/
docker rm -f $plugin_container
#docker rmi $plugin_image

#build the images of conductor.
cd $tmppath/conductor/docker
docker-compose build
