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
   sleep 120
   heat stack-list
   heat stack-show bottlenecks
   nova list
   nova list | grep rubbos_control
   control_ip=$(nova list | grep rubbos_control | awk '{print $13}')
   ssh -i $KEY_PATH/bottlenecks_key \
       -o StrictHostKeyChecking=no \
       -o BatchMode=yes root@$control_ip "uname -a"
   heat stack-delete bottlenecks
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

bottlenecks_load_bottlenecks_image()
{
   echo "load bottlenecks image"

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

   echo "bottlenecks image id: $IMAGE_ID_BOTTLENECKS"
}

main()
{
   echo "create instances with heat template"

   BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks
   BOTTLENECKS_REPO_DIR=/tmp/opnfvrepo/bottlenecks
   IMAGE_URL=http://205.177.226.235:9999/bottlenecks/rubbos/bottlenecks-trusty-server.img
   IMAGE_NAME=bottlenecks-trusty-server
   KEY_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/bottlenecks_key
   HOT_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/heat_template
   KEY_NAME=bottlenecks-key
   FLAVOR_NAME=bottlenecks-flavor
   TEMPLATE_NAME=bottlenecks_rubbos_hot.yaml
   PUBLIC_NET_NAME=net04_ext

   bottlenecks_env_prepare
   bottlenecks_cleanup
   bottlenecks_load_bottlenecks_image
   bottlenecks_create_instance
   bottlenecks_cleanup
}

main
set +ex

