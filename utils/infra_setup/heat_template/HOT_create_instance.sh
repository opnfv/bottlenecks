#!/bin/bash

set -ex

bottlenecks_env_prepare()
{
    if [ -d $BOTTLENECKS_REPO_DIR ]; then
        rm -rf ${BOTTLENECKS_REPO_DIR}
    fi

    mkdir -p ${BOTTLENECKS_REPO_DIR}
    git config --global http.sslVerify false
    git clone ${BOTTLENECKS_REPO} ${BOTTLENECKS_REPO_DIR}

    source $BOTTLENECKS_REPO_DIR/rubbos/rubbos_scripts/1-1-1/scripts/env_preparation.sh
}

bottlenecks_check_instance()
{
    echo "check instance"
    heat stack-list
    heat stack-show bottlenecks
    nova list
    nova list | grep rubbos_control
}

bottlenecks_create_instance()
{
    echo "create bottlenecks instance using heat template"

    echo "upload keypair"
    nova keypair-add --pub_key $KEY_PATH/bottlenecks_key.pub $KEY_NAME

    echo "create flavor"
    nova flavor-create $FLAVOR_NAME 200 2048 10 1

    echo "use heat template to create stack"
    cd $HOT_PATH
    heat stack-create bottlenecks -f ${TEMPLATE_NAME} \
         -P "image=$IMAGE_NAME;key_name=$KEY_NAME;public_net=$PUBLIC_NET_NAME;flavor=$FLAVOR_NAME"
}

bottlenecks_rubbos_cirros_run()
{
    echo "Run Rubbos based on cirros image"
    control_ip=$(nova list | grep rubbos_control | awk '{print $13}')
    for i in rubbos_benchmark rubbos_client1 rubbos_client2 rubbos_client3 \
             rubbos_client4 rubbos_control rubbos_httpd rubbos_mysql1 \
             rubbos_tomcat1
    do
          ip=$(nova list | grep $i | awk '{print $12}' | awk -F [=,] '{print $2}')
          echo "$i=$ip" >> $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
    done

    chmod 600 $KEY_PATH/bottlenecks_key
    ssh -i $KEY_PATH/bottlenecks_key \
        -o StrictHostKeyChecking=no \
        -o BatchMode=yes cirros@$control_ip "uname -a"
    scp -r -i $KEY_PATH/bottlenecks_key \
        -o StrictHostKeyChecking=no -o BatchMode=yes \
        $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup \
        cirros@$control_ip:/tmp
    ssh -i $KEY_PATH/bottlenecks_key \
        -o StrictHostKeyChecking=no \
        -o BatchMode=yes cirros@$control_ip "bash /tmp/vm_dev_setup/setup_env.sh"

    rm -rf $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
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

    chmod 600 $KEY_PATH/bottlenecks_key
    ssh -i $KEY_PATH/bottlenecks_key \
        -o StrictHostKeyChecking=no \
        -o BatchMode=yes ec2-user@$control_ip "uname -a"
    scp -r -i $KEY_PATH/bottlenecks_key \
        -o StrictHostKeyChecking=no -o BatchMode=yes \
        $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup \
        ec2-user@$control_ip:/tmp
    ssh -i $KEY_PATH/bottlenecks_key \
        -o StrictHostKeyChecking=no \
        -o BatchMode=yes ec2-user@$control_ip "bash /tmp/vm_dev_setup/setup_env.sh"

    rm -rf $BOTTLENECKS_REPO_DIR/utils/infra_setup/vm_dev_setup/hosts.conf
}

bottlenecks_cleanup()
{
    echo "clean up bottlenecks images and keys"

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
}

bottlenecks_load_cirros_image()
{
    echo "load cirros image"

    wget http://download.cirros-cloud.net/0.3.3/cirros-0.3.3-x86_64-disk.img -O \
             /tmp/bottlenecks-cirros.img

    result=$(glance image-create \
        --name $IMAGE_NAME \
        --disk-format qcow2 \
        --container-format bare \
        --file /tmp/bottlenecks-cirros.img)
    echo "$result"

    rm -rf /tmp/bottlenecks-cirros.img

    IMAGE_ID_BOTTLENECKS=$(echo "$result" | grep " id " | awk '{print $(NF-1)}')
    if [ -z "$IMAGE_ID_BOTTLENECKS" ]; then
         echo 'failed to upload bottlenecks image to openstack'
         exit 1
    fi

    echo "bottlenecks image id: $IMAGE_ID_BOTTLENECKS"
}

bottlenecks_load_bottlenecks_image()
{
    echo "load bottlenecks image"

#    curl --connect-timeout 10 -o /tmp/bottlenecks-trusty-server.img $IMAGE_URL -v

    wget https://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img -O \
              /tmp/bottlenecks-trusty-server.img

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

    echo "bottlenecks image id: $IMAGE_ID_BOTTLENECKS"
}

main()
{
    echo "create instances with heat template"

    BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks
    BOTTLENECKS_REPO_DIR=/tmp/opnfvrepo/bottlenecks
    IMAGE_URL=http://artifacts.opnfv.org/bottlenecks/rubbos/bottlenecks-trusty-server.img
    IMAGE_NAME=bottlenecks-trusty-server
    KEY_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/bottlenecks_key
    HOT_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/heat_template
    KEY_NAME=bottlenecks-key
    FLAVOR_NAME=bottlenecks-flavor
    TEMPLATE_NAME=bottlenecks_rubbos_hot.yaml
    PUBLIC_NET_NAME=net04_ext

    bottlenecks_env_prepare
    bottlenecks_cleanup
    bottlenecks_load_cirros_image
    bottlenecks_create_instance
    sleep 120
    bottlenecks_check_instance
    bottlenecks_rubbos_cirros_run
    bottlenecks_cleanup
    bottlenecks_load_bottlenecks_image
    bottlenecks_create_instance
    sleep 600
    bottlenecks_check_instance
    bottlenecks_rubbos_run
    bottlenecks_cleanup
}

main
set +ex
