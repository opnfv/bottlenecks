#!/bin/bash

set -e

bottlenecks_create_instance()
{
   echo "create bottlenecks instance using heat template"

   mkdir -p ${BOTTLENECKS_REPO_DIR}
   git config --global http.sslVerify false
   git clone ${BOTTLENECKS_REPO} ${BOTTLENECKS_REPO_DIR}

   echo "upload keypair"
   nova keypair-add --pub_key $KEY_PATH/bottleneck_key.pub $KEY_NAME
   #need FIX, only upload the public key? should be keypair

   echo "use heat template to create stack"
   heat stack-create bottlenecks -f ${TEMPLATE_NAME} -P "image=$IMAGE_NAME;key=$KEY_NAME;public_network=$PUBLIC_NET_NAME"
   #need FIX, use stack to create 9 VMs
}

bottlenecks_cleanup()
{
   echo "clean up bottlenecks images"

   if ! glance image-list; then
       return
   fi

   #need to check
   for image in $(glance image-list | grep -e $IMAGE_NAME | awk '{print $2}'); do
       echo "clean up image $image"
       glance image-delete $iamge || true
   done

   #FIX ME
   #nova flavor-delete yardstick-flavor &> /dev/null || true
}

bottlenecks_build_image()
{
   echo "build bottlenecks image"

   #need FIX
}

bottlenecks_load_cirros_image()
{
   echo "load bottlenecks cirros image"

   local image_file=/home/opnfv/images/cirros-0.3.3-x86_64-disk.img

   result=$(glance image-create \
       --name cirros-0.3.3 \
       --disk-format qcow2 \
       --container-format bare \
       --file $image_file)
   echo "$result"

   IMAGE_ID_CIRROS=$(echo "$output" | grep " id " | awk '{print $(NF-1)}')
   if [ -z "$IMAGE_ID_CIRROS" ]; then
        echo 'failed to upload cirros image to openstack'
        exit 1
   fi

   echo "cirros image id: $IMAGE_ID_CIRROS"
}

bottlenecks_load_image()
{
   echo "load bottlenecks image"

   result=$(glance --os-image-api-version 1 image-create \
      --name $IMAGE_NAME \
      --is-public true --disk-format qcow2 \
      --container-format bare \
      --file $IMAGE_FILE_NAME)
   echo "$result"

   GLANCE_IMAGE_ID=$(echo "$result" | grep " id " | awk '{print $(NF-1)}')

   if [ -z "$GLANCE_IMAGE_ID" ]; then
       echo 'add image to glance failed'
       exit 1
   fi

   sudo rm -f $IMAGE_FILE_NAME

   echo "add glance image completed: $GLANCE_IMAGE_ID"
}

main()
{
   echo "create instances with heat template"

   BOTTLENECKS_REPO=https://gerrit.opnfv.org/gerrit/bottlenecks
   BOTTLENECKS_REPO_DIR=/tmp/opnfvrepo/bottlenecks
   #IMAGE_URL=http://205.177.226.235:9999
   IMAGE_NAME=bottleneks_ubuntu
   #need FIX, need a script to transfer the image from the url to be the installer images
   KEY_PATH=$BOTTLENECKS_REPO_DIR/utils/infra_setup/bottlenecks_key
   KEY_NAME=bottlenecks_key
   TEMPLATE_NAME=bottlenecks_template1.yaml
   PUBLIC_NET_NAME=net04_ext
   #need FIX
   IMAGE_FILE_NAME=""

   #bottlenecks_cleanup
   #bottlenecks_build_image
   bottlenecks_load_cirros_image
   bottlenecks_create_instance
}

main
