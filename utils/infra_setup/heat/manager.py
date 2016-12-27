##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import time
import common as op_utils
from glanceclient.client import Client as GlanceClient
from novaclient.client import Client as NovaClient


def _get_glance_client():
    sess = op_utils.get_session()
    return GlanceClient(
        op_utils.get_glance_api_version(),
        session=sess)


def _get_nova_client():
    sess = op_utils.get_session()

    return NovaClient(
        op_utils.get_nova_api_version(),
        session=sess)


def stack_create_images(
        imagefile=None,
        image_name="bottlenecks_image"):
    print "========== Create image in OS =========="

    if imagefile is None:
        print "imagefile not set/found"
        return False

    glance = _get_glance_client()
    image = glance.images.create(
        name=image_name,
        disk_format="qcow2",
        container_format="bare")
    with open(imagefile) as fimage:
        glance.images.upload(image.id, fimage)

    timeInQueue = 0
    img_status = image.status
    while img_status == "queued" and timeInQueue < 30:
        print "  image's status: " + img_status
        time.sleep(1)
        timeInQueue = timeInQueue + 1
        img_status = glance.images.get(image.id).status

    print "After %d seconds,image status is [%s]" % (timeInQueue, img_status)
    return True if img_status == "active" else False


def stack_create_keypairs(key_path, name="bottlenecks_keypair"):
    print "========== Add keypairs in OS =========="
    nova = _get_nova_client()
    with open(key_path) as pkey:
        nova.keypairs.create(name=name, public_key=pkey.read())


def stack_create_flavors(
        name="bottlenecks_flavor",
        ram=4096,
        vcpus=2,
        disk=10):
    print "========== Create flavors in OS =========="
    nova = _get_nova_client()
    nova.flavors.create(name=name, ram=ram, vcpus=vcpus, disk=disk)
