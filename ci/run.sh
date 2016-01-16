#!/bin/bash

set -ex

SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`
export BOTTLENECKS_TOP_DIR=$SCRIPT_DIR/../
export GERRIT_REFSPEC_DEBUG=$1

$SCRIPT_DIR/rubbos_docker_run.sh

set +ex

