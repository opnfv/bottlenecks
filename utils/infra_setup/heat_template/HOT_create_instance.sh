#!/bin/bash

set -x

GERRIT_REFSPEC_DEBUG=$1

bottlenecks_env_prepare()
{
    echo "Bottlenecks env prepare start $(date)"

    #if [ -d $BOTTLENECKS_REPO_DIR ]; then
    #    rm -rf ${BOTTLENECKS_REPO_DIR}
    #fi

    #mkdir -p ${BOTTLENECKS_REPO_DIR}
    #git config --global http.sslVerify false
    #git clone ${BOTTLENECKS_REPO} ${BOTTLENECKS_REPO_DIR}
    if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
        cd ${BOTTLENECKS_REPO_DIR}
        git fetch $BOTTLENECKS_REPO $GERRIT_REFSPEC_DEBUG && git checkout FETCH_HEAD
        cd -
    fi

    source $BOTTLENECKS_REPO_DIR/rubbos/rubbos_scripts/1-1-1/scripts/env_preparation.sh
    chmod 600 $KEY_PATH/bottlenecks_key

    echo "Bottlenecks env prepare end $(date)"
}

wait_heat_stack_complete() {
    retry=0
    while true
    do
        status=$(heat stack-list | grep bottlenecks | awk '{print $6}')
        if [ x$status = x"CREATE_COMPLETE" ]; then
            echo "bottlenecks stacke create complete"
            heat stack-show bottlenecks
            nova list | grep rubbos_
            break;
        elif [ x$status = x"CREATE_FAILED" ]; then
            echo "bottlenecks stacke create failed !!!"
            heat stack-show bottlenecks
            exit 1
        fi

        #if [ $BOTTLENECKS_DEBUG = True ]; then
        if false; then
            heat stack-show bottlenecks
            nova list | grep rubbos_
            for i in $(nova list | grep rubbos_ | grep ERROR | awk '{print $2}')
            do
                 nova show $i
            done
        fi
        sleep 1
        let retry+=1
        if [[ $retry -ge $1 ]];then
            echo "Heat stack create timeout, status $status !!!"
            exit 1
        fi
    done
}

wait_rubbos_control_ok() {
    control_ip=$(nova list | grep rubbos_control | awk '{print $13}')

    retry=0
    until timeout 3s ssh $ssh_args ubuntu@$control_ip "exit" >/dev/null 2>&1
    do
        echo "retry connect rubbos control $retry"
        sleep 1
        let retry+=1
        if [[ $retry -ge $1 ]];then
            echo "rubbos control start timeout !!!"
            exit 1
        fi
    done
    ssh $ssh_args ubuntu@$control_ip "uname -a"
}

bottlenecks_check_instance_ok()
{
    echo "Bottlenecks check instance ok start $(date)"

    wait_heat_stack_complete 120
    wait_rubbos_control_ok 300
    nova list | grep rubbos_
    if [ $BOTTLENECKS_DEBUG = True ]; then
        date
        while true
        do
            for i in rubbos_benchmark rubbos_client1 rubbos_client2 rubbos_client3 \
                     rubbos_client4 rubbos_control rubbos_httpd rubbos_mysql1 rubbos_tomcat1
            do
               echo "logging $i"
               nova console-log $i | tail -n 2 | grep Cloud-init | grep finished
               if [ $? != 0 ]; then
                   break
               fi
               if [ $i = rubbos_tomcat1 ]; then
                   echo "all vm Cloud-init finished!"
                   date
                   return
               fi
            done
            sleep 10
        done
    fi

    echo "Bottlenecks check instance ok end $(date)"
}

bottlenecks_create_instance()
{
    echo "Bottlenecks create instance using heat template start $(date)"

    echo "upload keypair"
    nova keypair-add --pub_key $KEY_PATH/bottlenecks_key.pub $KEY_NAME

    echo "create flavor"
    nova flavor-create $FLAVOR_NAME 200 4096 20 2

    echo "use heat template to create stack"
    cd $HOT_PATH
    heat stack-create bottlenecks -f ${TEMPLATE_NAME} \
         -P "image=$IMAGE_NAME;key_name=$KEY_NAME;public_net=$PUBLIC_NET_NAME;flavor=$FLAVOR_NAME"

    echo "Bottlenecks create instance using heat template end $(date)"
}

bottlenecks_rubbos_wait_finish()
{
    echo "Start checking rubbos running status..."
    retry=0
    while true
    do
        ssh $ssh_args ubuntu@$control_ip "FILE=/tmp/rubbos_finished; if [ -f \$FILE ]; then exit 0; else exit 1; fi"
        if [ $? = 0 ]; then
            echo "Rubbos test case successfully finished :)"
            return 0
        fi
        echo "Rubbos running $retry ..."
        sleep 30
        let retry+=1
        if [[ $retry -ge $1 ]]; then
            echo "Rubbos test case timeout :("
            return 1
        fi
    done
}

bottlenecks_rubbos_run()
{
    echo "Run Rubbos"
    control_ip=$(nova list | grep rubbos_control | awk '{print $13}')
    for i in rubbos_benchmark rubbos_client1 rubbos_client2 rubbos_client3 \
             rubbos_client4 rubbos_control rubbos_httpd rubbos_mysql1 \
             rubbos_tomcat1
    do
          ip=$(nova list | grep $i | awk '{print $12}' | awk -F [=,] '{print $2}')
          echo "$i=$ip" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    done

    nameserver_ip=$(grep -m 1 '^nameserver' \
        /etc/resolv.conf | awk '{ print $2 '})
    echo "nameserver_ip=$nameserver_ip" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf

    echo "GERRIT_REFSPEC_DEBUG=$GERRIT_REFSPEC_DEBUG" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf

    echo "POD_NAME=$POD_NAME" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    echo "INSTALLER_TYPE=$INSTALLER_TYPE" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    echo "BOTTLENECKS_VERSION=$BOTTLENECKS_VERSION" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    echo "BOTTLENECKS_DB_TARGET=$BOTTLENECKS_DB_TARGET" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf

    scp $ssh_args -r \
        $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup \
        ubuntu@$control_ip:/tmp
    ssh $ssh_args \
        ubuntu@$control_ip "bash /tmp/vm_dev_setup/setup_env.sh" &

    bottlenecks_rubbos_wait_finish 200

    rm -rf $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
}

bottlenecks_cleanup()
{
    echo "Bottlenecks cleanup start $(date)"

    if heat stack-list; then
        for stack in $(heat stack-list | grep -e bottlenecks | awk '{print $2}'); do
            echo "clean up stack $stack"
            heat stack-delete $stack || true
            sleep 30
        done
    fi

    if glance image-list; then
        for image in $(glance image-list | grep -e $IMAGE_NAME | awk '{print $2}'); do
            echo "clean up image $image"
            glance image-delete $image || true
        done
    fi

    if nova keypair-list; then
        for key in $(nova keypair-list | grep -e $KEY_NAME | awk '{print $2}'); do
            echo "clean up key $key"
            nova keypair-delete $key || true
        done
    fi

    if nova flavor-list; then
        for flavor in $(nova flavor-list | grep -e $FLAVOR_NAME | awk '{print $2}'); do
            echo "clean up flavor $flavor"
            nova flavor-delete $flavor || true
        done
    fi

    echo "Bottlenecks cleanup end $(date)"
}

bottlenecks_load_bottlenecks_image()
{
    echo "Bottlenecks load image start $(date)"

    curl --connect-timeout 10 -o /tmp/bottlenecks-trusty-server.img $IMAGE_URL -v

    result=$(glance image-create \
        --name $IMAGE_NAME \
        --disk-format qcow2 \
        --container-format bare \
        --file /tmp/bottlenecks-trusty-server.img)
    echo "$result"

    #rm -rf /tmp/bottlenecks-trusty-server.img

    IMAGE_ID_BOTTLENECKS=$(echo "$result" | grep " id " | awk '{print $(NF-1)}')
    if [ -z "$IMAGE_ID_BOTTLENECKS" ]; then
         echo 'failed to upload bottlenecks image to openstack'
         exit 1
    fi

    echo "bottlenecks image end id: $IMAGE_ID_BOTTLENECKS $(date)"
}

main()
{
    echo "main start $(date)"

    BOTTLENECKS_DEBUG=True
    BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks
    BOTTLENECKS_REPO_DIR=/tmp/opnfvrepo/bottlenecks
    IMAGE_URL=http://artifacts.opnfv.org/bottlenecks/rubbos/bottlenecks-trusty-server.img
    #IMAGE_URL=https://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img
    IMAGE_NAME=bottlenecks-trusty-server
    KEY_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/bottlenecks_key
    HOT_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/heat_template
    KEY_NAME=bottlenecks-key
    FLAVOR_NAME=bottlenecks-flavor
    TEMPLATE_NAME=bottlenecks_rubbos_hot.yaml
    #TODO use EXTERNAL_NET
    PUBLIC_NET_NAME=ext-net
    ssh_args="-o StrictHostKeyChecking=no -o BatchMode=yes -i $KEY_PATH/bottlenecks_key"
    : ${POD_NAME:='opnfv-jump-2'}
    : ${INSTALLER_TYPE:='fuel'}
    : ${BOTTLENECKS_VERSION:='master'}
    #: ${BOTTLENECKS_DB_TARGET:='213.77.62.197'}
    : ${BOTTLENECKS_DB_TARGET:='213.77.62.19'}

    bottlenecks_env_prepare
    set -x
    bottlenecks_cleanup
    bottlenecks_load_bottlenecks_image
    bottlenecks_create_instance
    bottlenecks_check_instance_ok
    bottlenecks_rubbos_run
    #bottlenecks_cleanup
    echo "main end $(date)"
}

main
set +x

