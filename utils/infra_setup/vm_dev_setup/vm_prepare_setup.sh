#!/bain/bash

main()
{
    SCRIPT_DIR=`cd ${BASH_SOURCE[0]%/*};pwd`

    source $SCRIPT_DIR/package.conf
    source $SCRIPT_DIR/hosts.conf
    source $SCRIPT_DIR/common.sh

    generate_ssh_key
    configue_nameserver $nameserver_ip
    #install_packages $PreInstall_Packages
}

main

