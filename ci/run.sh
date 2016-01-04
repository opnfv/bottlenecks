#!/bin/bash

BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks

SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`
GERRIT_REFSPEC_DEBUG=$1

if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
    echo $GERRIT_REFSPEC_DEBUG
    git fetch $BOTTLENECKS_REPO $GERRIT_REFSPEC_DEBUG && git checkout FETCH_HEAD
fi

$SCRIPT_DIR/../utils/infra_setup/heat_template/HOT_create_instance.sh $GERRIT_REFSPEC_DEBUG

