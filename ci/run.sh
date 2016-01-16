#!/bin/bash

set -ex

BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks

export SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`
export GERRIT_REFSPEC_DEBUG=$1

if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
    git fetch $BOTTLENECKS_REPO $GERRIT_REFSPEC_DEBUG && git checkout FETCH_HEAD
fi

$SCRIPT_DIR/rubbos_docker_run.sh

set +ex

