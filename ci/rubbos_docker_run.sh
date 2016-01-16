#!/bin/bash

set -ex

docker build -t opnfv/bottlenecks ${BOTTLENECKS_TOP_DIR}/ci/docker/bottlenecks-ci/

if [ x"${GERRIT_REFSPEC_DEBUG}" != x ]; then
    opts="--privileged=true"
    BOTTLENECKS_BRANCH=${GERRIT_REFSPEC_DEBUG}
else
    opts="--privileged=true --rm"
    BOTTLENECKS_BRANCH=${GIT_BRANCH##origin/}
fi

envs="-e INSTALLER_TYPE=${INSTALLER_TYPE} -e INSTALLER_IP=${INSTALLER_IP} -e NODE_NAME=${NODE_NAME} -e EXTERNAL_NET=${EXTERNAL_NETWORK} -e BOTTLENECKS_BRANCH=${BOTTLENECKS_BRANCH} -e GERRIT_REFSPEC_DEBUG=${GERRIT_REFSPEC_DEBUG} -e BOTTLENECKS_DB_TARGET=${BOTTLENECKS_DB_TARGET} -e PACKAGE_URL=${PACKAGE_URL}"
volumes="-v ${BOTTLENECKS_TOP_DIR}:${BOTTLENECKS_TOP_DIR}"
create_instance=${BOTTLENECKS_TOP_DIR}/utils/infra_setup/heat_template/HOT_create_instance.sh

echo ${envs} ${ops} ${volumes}

# Run docker
cmd="sudo docker run ${opts} ${envs} ${volumes} opnfv/bottlenecks ${create_instance}"
echo "Bottlenecks: Running docker cmd: ${cmd}"
${cmd}

echo "Bottlenecks: done!"

set +ex

