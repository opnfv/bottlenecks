#!/bin/bash
##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
usage="Script to install and config golang of specific version.

usage:
    bash $(basename "$0") [-h|--help] [-v|--version <version>] [--debug]

where:
    -h|--help         show the help text
    -v|--version      input the version of golang
    --debug           debug option switch
examples:
    $(basename "$0") -v 1.10.3"

# Debug option
redirect="/dev/null"

# Process input variables
while [[ $# > 0 ]]
    do
    key="$1"
    case $key in
        -h|--help)
            echo "$usage"
            exit 0
            shift
        ;;
        -v|--version)
            GOLANG_VERSION="$2"
            shift
        ;;
        --debug)
            redirect="/dev/stdout"
            shift
        ;;
        *)
            echo "unkown option $1 $2"
            exit 1
        ;;
    esac
    shift
done

#set -e

echo "=======Downloading golang of version: ${GOLANG_VERSION}========"

if [[ -f go${GOLANG_VERSION}.linux-amd64.tar.gz ]]; then
    rm go${GOLANG_VERSION}.linux-amd64.tar.gz
fi
curl -O https://storage.googleapis.com/golang/go${GOLANG_VERSION}.linux-amd64.tar.gz >${redirect}

echo "Installing golang of version: ${GOLANG_VERSION}"
if [[ -d /usr/local/go ]]; then
    rm -rf /usr/local/go
fi

tar -C /usr/local -xzf go${GOLANG_VERSION}.linux-amd64.tar.gz >${redirect}

if [[ -d $HOME/go ]]; then
    rm -rf ${HOME}/go
    mkdir ${HOME}/go
    mkdir ${HOME}/go/bin
else
    mkdir ${HOME}/go
    mkdir ${HOME}/go/bin
fi

echo "Adding golang env to ~/.bashrc"
GOROOT=/usr/local/go
GOPATH=${HOME}/go

if [[ $(cat ${HOME}/.bashrc | grep GOROOT) ]]; then
    echo "golang env alreay in ${HOME}/.bashrc"
else
   cat <<EOF >> ${HOME}/.bashrc

export GOROOT=/usr/local/go
export GOPATH=${HOME}/go
export PATH=${PATH}:${GOROOT}/bin:${GOPATH}/bin
EOF
fi

export GOROOT=/usr/local/go
export GOPATH=${HOME}/go
export PATH=${PATH}:${GOROOT}/bin:${GOPATH}/bin

echo "Running go version command:"
go version

echo "=======Installation of golang-${GOLANG_VERSION} complete======="

