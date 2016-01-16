#!/bin/bash

set -ex

docker build -t opnfv/bottlenecks $SCRIPT_DIR/docker/bottlenecks-ci/

if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
    opts="--privileged=true"
else
    opts="--privileged=true --rm"
fi

envs="-e INSTALLER_TYPE=${INSTALLER_TYPE} -e INSTALLER_IP=${INSTALLER_IP} -e NODE_NAME=${NODE_NAME} -e EXTERNAL_NETWORK=${EXTERNAL_NETWORK} -e BOTTLENECKS_BRANCH=${GIT_BRANCH##origin/} -e GERRIT_REFSPEC_DEBUG=${GERRIT_REFSPEC_DEBUG}"

echo $envs $ops
#$SCRIPT_DIR/../utils/infra_setup/heat_template/HOT_create_instance.sh

set +ex

