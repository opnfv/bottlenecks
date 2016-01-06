#!/bin/bash

set -ex

GERRIT_REFSPEC_DEBUG=$1

echo "vstf DEBUG test"
echo "vstf workflow goes here"

bottlenecks_env_prepare()
{
    if [ -d $BOTTLENECKS_REPO_DIR ]; then
        rm -rf ${BOTTLENECKS_REPO_DIR}
    fi

    mkdir -p ${BOTTLENECKS_REPO_DIR}
    git config --global http.sslVerify false
    git clone ${BOTTLENECKS_REPO} ${BOTTLENECKS_REPO_DIR}
    if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
        cd ${BOTTLENECKS_REPO_DIR}
        git fetch $BOTTLENECKS_REPO $GERRIT_REFSPEC_DEBUG && git checkout FETCH_HEAD
        cd -
    fi

    #obtain installer(openstack) IP, etc, use rubbos's temporarily, later we can amend this
    source $BOTTLENECKS_REPO_DIR/rubbos/rubbos_scripts/1-1-1/scripts/env_preparation.sh
}

#vstf logic function here

main()
{
    echo "bottlenecks vstf: create instances with heat template"

    BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks
    BOTTLENECKS_REPO_DIR=/tmp/opnfvrepo/bottlenecks
    #vstf parameter here

    bottlenecks_env_prepare
    #vstf function here
}

main
set +ex
