#!/bin/bash
##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -x

git_checkout()
{
    if git cat-file -e $1^{commit} 2>/dev/null; then
        # branch, tag or sha1 object
        git checkout $1
    else
        # refspec / changeset
        git fetch --tags --progress $2 $1
        git checkout FETCH_HEAD
    fi
}

bottlenecks_env_prepare() {
    set -e
    echo "Bottlenecks env prepare start $(date)"
    git config --global http.sslVerify false

    if [ ! -d $BOTTLENECKS_REPO_DIR ]; then
        git clone $BOTTLENECKS_REPO $BOTTLENECKS_REPO_DIR
    fi
    cd $BOTTLENECKS_REPO_DIR
    git checkout master && git pull
    git_checkout $BOTTLENECKS_BRANCH $BOTTLENECKS_REPO
    cd -

    echo "Creating openstack credentials .."
    if [ ! -d $RELENG_REPO_DIR ]; then
        git clone $RELENG_REPO $RELENG_REPO_DIR
    fi
    cd $RELENG_REPO_DIR
    git checkout master && git pull
    git_checkout $RELENG_BRANCH $RELENG_REPO
    cd -

    # Create openstack credentials
    $RELENG_REPO_DIR/utils/fetch_os_creds.sh \
        -d /tmp/openrc \
        -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}

    source /tmp/openrc

    chmod 600 $KEY_PATH/bottlenecks_key

    echo "Bottlenecks env prepare end $(date)"
    set +e
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
         -P "image=$IMAGE_NAME;key_name=$KEY_NAME;public_net=$EXTERNAL_NET;flavor=$FLAVOR_NAME"

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
    echo "BOTTLENECKS_BRANCH=$BOTTLENECKS_BRANCH" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf

    echo "NODE_NAME=$NODE_NAME" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    echo "INSTALLER_TYPE=$INSTALLER_TYPE" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    echo "BOTTLENECKS_VERSION=$BOTTLENECKS_VERSION" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    echo "BOTTLENECKS_DB_TARGET=$BOTTLENECKS_DB_TARGET" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    echo "PACKAGE_URL=$PACKAGE_URL" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf

    scp $ssh_args -r \
        $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup \
        ubuntu@$control_ip:/tmp
    ssh $ssh_args \
        ubuntu@$control_ip "bash /tmp/vm_dev_setup/setup_env.sh" &

    bottlenecks_rubbos_wait_finish 200

    if [ x"$GERRIT_REFSPEC_DEBUG" != x ]; then
        # TODO fix hard coded path
        scp $ssh_args \
            ubuntu@$control_ip:"/bottlenecks/rubbos/rubbos_results/2015-01-20T081237-0700.tgz" /tmp
    fi

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

    rm -rf /tmp/bottlenecks-trusty-server.img

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

    : ${BOTTLENECKS_DEBUG:='True'}
    : ${BOTTLENECKS_REPO:='https://gerrit.opnfv.org/gerrit/bottlenecks'}
    : ${BOTTLENECKS_REPO_DIR:='/tmp/opnfvrepo/bottlenecks'}
    : ${BOTTLENECKS_BRANCH:='master'} # branch, tag, sha1 or refspec
    : ${RELENG_REPO:='https://gerrit.opnfv.org/gerrit/releng'}
    : ${RELENG_REPO_DIR:='/tmp/opnfvrepo/releng'}
    : ${RELENG_BRANCH:='master'} # branch, tag, sha1 or refspec
    : ${IMAGE_NAME:='bottlenecks-trusty-server'}
    KEY_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/bottlenecks_key
    HOT_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/heat_template
    : ${KEY_NAME:='bottlenecks-key'}
    : ${FLAVOR_NAME:='bottlenecks-flavor'}
    : ${TEMPLATE_NAME:='bottlenecks_rubbos_hot.yaml'}
    ssh_args="-o StrictHostKeyChecking=no -o BatchMode=yes -i $KEY_PATH/bottlenecks_key"
    : ${EXTERNAL_NET:='net04_ext'}
    : ${PACKAGE_URL:='http://artifacts.opnfv.org/bottlenecks'}
    : ${NODE_NAME:='opnfv-jump-2'}
    : ${INSTALLER_TYPE:='fuel'}
    : ${INSTALLER_IP:='10.20.0.2'}
    # TODO fix for dashboard
    : ${BOTTLENECKS_VERSION:='master'}
    : ${BOTTLENECKS_DB_TARGET:='213.77.62.197'}
    IMAGE_URL=${PACKAGE_URL}/rubbos/bottlenecks-trusty-server.img

    bottlenecks_env_prepare
    set -x
    bottlenecks_cleanup
    bottlenecks_load_bottlenecks_image
    bottlenecks_create_instance
    bottlenecks_check_instance_ok
    bottlenecks_rubbos_run
    bottlenecks_cleanup
    echo "main end $(date)"
}

main
set +x

