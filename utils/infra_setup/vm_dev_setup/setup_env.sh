#!/bin/bash

set -ex

bottlenecks_prepare_env()
{
    set +e
    for i in $PreInstall_Packages; do
        if ! apt --installed list 2>/dev/null |grep "\<$i\>"
        then
            sudo apt-get install  -y --force-yes  $i
        fi
    done
    set -e

    if [ -d $RUBBOS_CACHE_DIR ]; then
        rm -rf $RUBBOS_CACHE_DIR
    fi
    mkdir -p $RUBBOS_CACHE_DIR
}

bottlenecks_download_repo()
{
    if [-d $BOTTELENECKS_REPO_DIR/.git ]; then
        cd $BOTTLENECKS_REPO_DIR
        git pull origin master
        cd -
    else
        rm -rf $BOTTLENECKS_REPO_DIR
        git clone $BOTTLENECKS_REPO $BOTTLENECKS_REPO_DIR
    fi
}

bottlenecks_download_packages()
{
    for i in ; do #list the packages
       if [[ ! $i ]]; then
           continue
       fi
       curl --connect-timeout 10 -o $RUBBOS_CACHE_DIR/$i $PACKAGE_URL 2>/dev/null
    done
}

bottlenecks_rubbos_install_exe()
{
    cd $RUBBOS_RUN_DIR
    ./run.sh
    cd $RUBBOS_EXE_DIR
    ./CONTROL_rubbos_exec.sh
}

main()
{
    PreInstall_Packages="gcc gettext g++ libaio1 libaio-dev make"
    SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`

    source $SCRIPT_DIR/package.conf

    #bottlenecks_prepare_env
    bottlenecks_download_repo
    bottlenecks_download_packages
    bottlenecks_rubbos_install_exe
}

main
