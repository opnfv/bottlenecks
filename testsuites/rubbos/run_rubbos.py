#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import argparse
import time
import heatclient
import keystoneclient
import glanceclient
import novaclient

#------------------------------------------------------
# parser for configuration files in each test case
# ------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf",
                    help="configuration files for the testcase, in yaml format",
                    default="rubbos_1-1-1.yaml")
args = parser.parse_args()

#--------------------------------------------------
# logging configuration
#--------------------------------------------------
logger = logging.getLogger('run_rubbos')
logger.setLevel(logging.DEBUG)

def _get_keystone_client():
    keystone_client = keystoneclient.v2_0.client.Client(
                auth_url=os.environ.get('OS_AUTH_URL'),
                username=os.environ.get('OS_USERNAME'),
                password=os.environ.get('OS_PASSWORD'),
                tenant_name=os.environ.get('OS_TENANT_NAME'),
                cacert=os.environ.get('OS_CACERT'))
    return keystone_client

def _get_heat_client():
    keystone = _get_keystone_client()
    heat_endpoint = keystone.service_catalog.url_for(service_type='orchestration')
    heat_client = heatclient.client.Client('1', endpoint=heat_endpoint, token=keystone.auth_token)

    return heat_client

def _get_glance_client():
    keystone = _get_keystone_client()
    glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                       endpoint_type='publicURL')
    return glanceclient.v2.client.Client(glance_endpoint, token=keystone.auth_token)

def _get_nova_client():
    nova_client = novaclient.client.Client("2", auth_url=os.environ.get('OS_AUTH_URL'),
                username=os.environ.get('OS_USERNAME'),
                password=os.environ.get('OS_PASSWORD'),
                tenant_name=os.environ.get('OS_TENANT_NAME'),
                region_name=os.environ.get('OS_REGION_NAME'),
                cacert=os.environ.get('OS_CACERT'))
    return nova_client

def download_url(url, dest_path):
    """
    Download a file to a destination path given a URL
    """
    name = url.rsplit('/')[-1]
    dest = dest_path + "/" + name
    try:
        response = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError):
        return False

    with open(dest, 'wb') as f:
        shutil.copyfileobj(response, f)
    return True

def rubbos_env_prepare(template=None):
    """ Prepare for rubbos running env
    """
    #logger.info("generate heat template for the testcase based on template '%s'." % template)
    pass

def rubbos_env_cleanup():
    glance = _get_glance_client()
    heat = _get_heat_client()
    nova = _get_nova_client()

    for stack in self.heat.stacks.list():
        heat.stacks.delete(stack.id)

    for image in self.glance.images.list():
        glance.images.delete(image.id)

    for keypair in self.nova.keypairs.list():
        nova.keypairs.delete(keypair.id)

    for flavor in self.nova.flavors.list():
        nova.flavors.delete(flavor.id)

    logger.info("openstack env cleanup")

def rubbos_load_image(name=None):
    file_url = '/tmp'
    download_url(image_url,file_url)

    glance = _get_glance_client()
    image_args = {'name': name,
                  'disk-format': 'qcow2',
                  'container_format': 'bare',
                  'file': '/tmp/bottlenecks-trusty-server.img'}
    image = glance.images.create(**image_args)
    if not (image.id):
       logger.error("failed to upload rubbos image to openstack")
       exit(-1)

def rubbos_create_instance(template_file=None, rubbos_parameters=None):
    heat = _get_heat_client()
    template = open(template_file, 'r')
    rubbos_stack = heat.stacks.create(stack_name='rubbos', template=template.read(), parameters=rubbos_parameters)
    uid = rubbos_stack['stack']['id']

def rubbos_stack_check(stack_name=None):
    for stack in heat.stacks.list():
        if stack.stack_name == stack_name:
           return stack.stack_status
    return 'NOT_FOUND'

def rubbos_run():
    pass

def main():
    global Heat_template
    global image_name
    global keyname
    global external_net
    global image_url
    image_name = 'rubbos'
    keyname = 'rubbos-key'
    external_net = 'net04_ext'
    image_url = 'http://artifacts.opnfv.org/bottlenecks/rubbos/bottlenecks-trusty-server.img'

    if not (args.conf):
       logger.error("configuration files are not set for testcase")
       exit(-1)
    else:
       Heat_template = args.conf

    parameters={image: image_name,
                key_name: keyname,
                public_net: external_net}

    rubbos_env_prepare(Heat_template)
    rubbos_env_cleanup()
    rubbos_load_image(name='rubbos')
    rubbos_create_instance(template_file=Heat_template, rubbos_paramters=parameters)
    time.sleep(400)
    rubbos_stack_check(stack_name='rubbos')
    rubbos_run()
    rubbos_env_cleanup()

if __name__=='__main__':
    main()
