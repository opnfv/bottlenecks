#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -ex

docker build -t opnfv/bottlenecks ${BOTTLENECKS_TOP_DIR}/ci/docker/

if [ x"${GERRIT_REFSPEC_DEBUG}" != x ]; then
    opts="--privileged=true"
    BOTTLENECKS_BRANCH=${GERRIT_REFSPEC_DEBUG}
else
    opts="--privileged=true --rm"
    BOTTLENECKS_BRANCH=${GIT_BRANCH##origin/}
fi

envs="-e INSTALLER_TYPE=${INSTALLER_TYPE} -e INSTALLER_IP=${INSTALLER_IP} -e NODE_NAME=${NODE_NAME} -e EXTERNAL_NET=${EXTERNAL_NETWORK} -e BOTTLENECKS_BRANCH=${BOTTLENECKS_BRANCH} -e GERRIT_REFSPEC_DEBUG=${GERRIT_REFSPEC_DEBUG} -e BOTTLENECKS_DB_TARGET=${BOTTLENECKS_DB_TARGET} -e PACKAGE_URL=${PACKAGE_URL}"
volumes="-v ${BOTTLENECKS_TOP_DIR}:${BOTTLENECKS_TOP_DIR}"
run_rubbos_testsuite=${BOTTLENECKS_TOP_DIR}/ci/run_test.sh -s rubbos

echo ${envs} ${ops} ${volumes}

# Run docker
cmd="sudo docker run ${opts} ${envs} ${volumes} opnfv/bottlenecks ${run_rubbos_testsuite}"
echo "Bottlenecks: Running docker cmd: ${cmd}"
${cmd}

echo "Bottlenecks: done!"

set +ex

