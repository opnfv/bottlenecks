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

vstf_cleanup()
{
    echo "[INFO]Begin to clean up vstf heat-stack ,glance images and keypairs"
    if heat stack-list; then
        for stack in $(heat stack-list | grep -e " vstf " | awk '{print $2}'); do
            echo "[INFO]clean up stack $stack"
            heat stack-delete $stack || true
            sleep 30
        done
    fi
    
    if glance image-list; then
        for image in $(glance image-list | grep -e "${MANAGER_IMAGE_NAME}" -e "${AGENT_IMAGE_NAME}" | awk '{print $2}'); do
            echo "[INFO]clean up image $image"
            glance image-delete $image || true
        done
    fi

    if nova keypair-list; then
        for key in $(nova keypair-list | grep -e $KEY_NAME | awk '{print $2}'); do
            echo "[INFO]clean up key $key"
            nova keypair-delete $key || true
        done
    fi

    #check the default flavor m1.large existing
    flag=`nova flavor-list | grep "m1.large "`
    echo "[INFO]the flavor m1.large num is $flag"
    return 0
}

vstf_register()
{
    echo "[INFO]download vstf images"
    #download vstf-manager and vstf-agent image
    curl --connect-timeout 10 -o /tmp/vstf-manager.img $MANAGER_IMAGE_URL -v
    curl --connect-timeout 10 -o /tmp/vstf-agent.img $AGENT_IMAGE_URL -v
    
    #register
    echo "[INFO]register vstf manager and agent images"
    result=$(glance image-create \
        --name $MANAGER_IMAGE_NAME \
        --disk-format qcow2 \
        --container-format bare \
        --file /tmp/vstf-manager.img)
    echo "Manager image register result $result."

    result=$(glance image-create \
        --name $AGENT_IMAGE_NAME \
        --disk-format qcow2 \
        --container-format bare \
        --file /tmp/vstf-agent.img)
    echo "Agent image register result $result."

    rm -rf /tmp/vstf-manager.img;rm -rf /tmp/vstf-agent.img
}

#vstf logic function here
vstf_create_heat_template()
{
    echo "create vstf instance using heat template"
    echo "upload keypair"
    nova keypair-add --pub_key $KEY_PATH/bottlenecks_key.pub $KEY_NAME
    
    echo "use heat template to create stack"
    cd ${HOT_PATH}
    heat stack-create vstf -f ${TEMPLATE_NAME}

}

wait_heat_stack_complete()
{
    retry=0
    while true
    do
        status=$(heat stack-list | grep vstf | awk '{print $6}')
        if [ x$status = x"CREATE_COMPLETE" ]; then
            echo "vstf stacke create complete"
            heat stack-show vstf
            nova list | grep rubbos_
            break;
        elif [ x$status = x"CREATE_FAILED" ]; then
            echo "bottlenecks stacke create failed !!!"
            heat stack-show bottlenecks
            exit 1
        fi

        if [ $BOTTLENECKS_DEBUG = True ]; then
            heat stack-show vstf
            nova list | grep vstf-
            for i in $(nova list | grep vstf- | grep ERROR | awk '{print $2}')
            do
                 nova show $i
            done
        fi
        sleep 1
        let retry+=1
        if [[ $retry -ge $1 ]];then
            echo "Heat vstf stack create timeout, status $status !!!"
            exit 1
        fi
    done
}


vstf_check_instance_ok()
{
    wait_heat_stack_complete 120 
    return 0
}

vstf_launch_vstf()
{
    cd ${HOT_PATH}
    bash -x launch_vstf.sh
    
}

main()
{
    echo "bottlenecks vstf: create instances with heat template"

    BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks
    BOTTLENECKS_REPO_DIR=/tmp/opnfvrepo_vstf/bottlenecks
    #vstf parameter here
    MANAGER_IMAGE_URL=http://artifacts.opnfv.org/bottlenecks/vstf/vstf-manager.img
    AGENT_IMAGE_URL=http://artifacts.opnfv.org/bottlenecks/vstf/vstf-agent.img
    MANAGER_IMAGE_NAME="vstf-manager"
    AGENT_IMAGE_NAME="vstf-agent"
    KEY_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/bottlenecks_key
    HOT_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/heat_template/vstf_heat_template
    KEY_NAME=bottlenecks-key
    #use the default openstack flavor m1.large
    FLAVOR_NAME="m1.large"
    TEMPLATE_NAME=bottleneck_vstf.yaml
    PUBLIC_NET_NAME=net04_ext

    #load adminrc 
    bottlenecks_env_prepare

    #vstf function here
    vstf_cleanup
    #vstf_register
    #vstf_create_heat_template
    #vstf_check_instance_ok
    #sleep 100
    #vstf_launch_vstf
    #sleep 30
    #vstf_test
    #sleep 10
    #echo "[INFO]bottleneck vstf testsuite done ,results in the directory ${HOT_PATH}/result"
    
}

main
set +ex
