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
import logging
import urllib2
import shutil
from heatclient.client import Client as HeatClient
from keystoneclient.v2_0.client import Client as KeystoneClient
from glanceclient.v2.client import Client as GlanceClient
from novaclient.client import Client as NovaClient

#------------------------------------------------------
# parser for configuration files in each test case
# ------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf",
                    help="configuration files for the testcase, in yaml format",
                    default="/home/opnfv/bottlenecks/testsuites/rubbos/testcase_cfg/rubbos_1-1-1.yaml")
args = parser.parse_args()

#--------------------------------------------------
# logging configuration
#--------------------------------------------------
logger = logging.getLogger(__name__)


def _get_keystone_client():
    keystone_client = KeystoneClient(
                auth_url=os.environ.get('OS_AUTH_URL'),
                username=os.environ.get('OS_USERNAME'),
                password=os.environ.get('OS_PASSWORD'),
                tenant_name=os.environ.get('OS_TENANT_NAME'),
                cacert=os.environ.get('OS_CACERT'))
    return keystone_client

def _get_heat_client():
    keystone = _get_keystone_client()
    heat_endpoint = keystone.service_catalog.url_for(service_type='orchestration')
    heat_client = HeatClient('1', endpoint=heat_endpoint, token=keystone.auth_token)
    return heat_client

def _get_glance_client():
    keystone = _get_keystone_client()
    glance_endpoint = keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
    return GlanceClient(glance_endpoint, token=keystone.auth_token)

def _get_nova_client():
    nova_client = NovaClient("2", os.environ.get('OS_USERNAME'),
                                  os.environ.get('OS_PASSWORD'),
                                  os.environ.get('OS_TENANT_NAME'),
                                  os.environ.get('OS_AUTH_URL'))
    return nova_client

def _download_url(src_url, dest_dir):
    ''' Download a file to a destination path given a URL'''
    file_name = src_url.rsplit('/')[-1]
    dest = dest_dir + "/" + file_name
    try:
        response = urllib2.urlopen(src_url)
    except (urllib2.HTTPError, urllib2.URLError):
        return None

    with open(dest, 'wb') as f:
        shutil.copyfileobj(response, f)
    return file_name


def rubbos_stack_satisfy(name="bottlenecks_rubbos_stack", status="CREATE_COMPLETE"):
    heat = _get_heat_client()
    for stack in heat.stacks.list():
        if status == None and stack.stack_name == name:
            # Found target stack
            print "Found stack, name=" + str(stack.stack_name)
            return True
        elif stack.stack_name == name and stack.stack_status==status:
            print "Found stack, name=" + str(stack.stack_name) + ", status=" + str(stack.stack_status)
            return True
    return False

def rubbos_env_prepare(template=None):
    print "========== Prepare rubbos environment =========="
    logger.info("Generate heat template for the testcase based on template '%s'." % template)

def rubbos_env_cleanup():
    print "========== Cleanup rubbos environment =========="
    glance = _get_glance_client()
    heat = _get_heat_client()
    nova = _get_nova_client()

    for image in glance.images.list():
        if image.name.find("bottlenecks_rubbos") >= 0:
            print "Delete image, id:" + str(image.id) + ", name:" + str(image.name)
            glance.images.delete(image.id)

    for keypair in nova.keypairs.list():
        if keypair.name.find("bottlenecks_rubbos") >= 0:
            print "Delete keypair, id:" + str(keypair.id) + ", name:" + str(keypair.name)
            nova.keypairs.delete(keypair.id)

    for flavor in nova.flavors.list():
        if flavor.name.find("bottlenecks_rubbos") >= 0:
            print "Delete flavor, id:" + str(flavor.id) + ", name:" + str(flavor.name)
            nova.flavors.delete(flavor.id)

    for stack in heat.stacks.list():
        if stack.stack_name.find("bottlenecks_rubbos") >= 0:
            print "Delete stack, id: " + str(stack.id) + ", name:" + str(stack.stack_name)
            heat.stacks.delete(stack.id)

    timeInProgress = 0
    while rubbos_stack_satisfy(name="bottlenecks_rubbos_stack", status=None) and timeInProgress < 60:
        time.sleep(5)
        timeInProgress = timeInProgress + 5

    if rubbos_stack_satisfy(name="bottlenecks_rubbos_stack", status=None) == True:
        print "Failed to clean the stack"
        return False
    else:
        return True

def rubbos_create_images(src_url=None, image_name="bottlenecks_rubbos_image"):
    print "========== Create rubbos image in OS =========="
    dest_dir = '/tmp'
    file_name = _download_url(src_url, dest_dir)
    #file_name = "bottlenecks-trusty-server.img"
    if file_name == None:
       return False

    glance = _get_glance_client()
    imagefile = dest_dir + "/" + file_name
    image = glance.images.create(name=image_name, disk_format="qcow2", container_format="bare")
    with open(imagefile) as fimage:
        glance.images.upload(image.id, fimage)

    timeInQueue = 0
    img_status = image.status
    while img_status == "queued" and timeInQueue < 30:
        print "  image's status: " + img_status
        time.sleep(1)
        timeInQueue = timeInQueue + 1
        img_status = glance.images.get(image.id).status

    print "After %d seconds, the image's status is [%s]" %(timeInQueue, img_status)
    return True if img_status == "active" else False

def rubbos_create_keypairs(key_path, name="bottlenecks_rubbos_keypair"):
    print "========== Add rubbos keypairs in OS =========="
    nova = _get_nova_client()
    with open(key_path) as pkey:
        nova.keypairs.create(name=name, public_key=pkey.read())

def rubbos_create_flavors(name="bottlenecks_rubbos_flavor", ram=4096, vcpus=2, disk=10):
    print "========== Create rubbos flavors in OS =========="
    nova = _get_nova_client()
    nova.flavors.create(name=name, ram=ram, vcpus=vcpus, disk=disk)

def rubbos_create_instances(template_file, rubbos_parameters=None, stack_name="bottlenecks_rubbos_stack"):
    print "========== Create rubbos instances =========="
    heat = _get_heat_client()

    with open(template_file) as template:
        stack = heat.stacks.create(stack_name=stack_name, template=template.read(), parameters=rubbos_parameters)

    stack_id = stack['stack']['id']
    stack_status = heat.stacks.get(stack_id).stack_status

    print "Created stack, id=" + str(stack_id) + ", status=" + str(stack_status)

    timeInProgress= 0
    while stack_status == "CREATE_IN_PROGRESS" and timeInProgress < 150:
        print "  stack's status: %s, after %d seconds" %(stack_status, timeInProgress)
        time.sleep(5)
        timeInProgress = timeInProgress + 5
        stack_status = heat.stacks.get(stack_id).stack_status

    print "After %d seconds, the stack's status is [%s]" %(timeInProgress, stack_status)
    return True if stack_status == "CREATE_COMPLETE" else False

def get_instances(nova_client):
    try:
        instances = nova_client.servers.list(search_opts={'all_tenants': 1})
        return instances
    except Exception, e:
        print "Error [get_instances(nova_client)]:", e
        return None

def rubbos_run():
    print "========== run rubbos ==========="

    nova = _get_nova_client()

    instances = get_instances(nova)
    control_servers = []
    client_servers = []
    web_servers = []
    cjdbc_controller = []
    database_servers = []
    for instance in instances:
        name = getattr(instance, 'name')
        private_ip = [ x['addr'] for x in getattr(instance, 'addresses').itervalues().next() if x['OS-EXT-IPS:type'] == 'fixed']
	public_ip =  [ x['addr'] for x in getattr(instance, 'addresses').itervalues().next() if x['OS-EXT-IPS:type'] == 'floating']

        if name.find("control") > 0:
           control_servers.append(''.join(str(name)+':'+public_ip[0]+':'+private_ip[0]))
        if name.find("client") > 0:
           client_servers.append(''.join(str(name)+':'+private_ip[0]))
        if name.find("tomcat") > 0:
           web_servers.append(''.join(str(name)+':'+private_ip[0]))
        if name.find("cjdbc") > 0:
           cjdbc_controller.append(''.join(str(name)+':'+private_ip[0]))
        if name.find("mysql") > 0:
           database_servers.append(''.join(str(name)+':'+private_ip[0]))

    f = open('hosts.conf', 'w')
    print >> f, '[Controller]'
    print >> f, 'controller =',
    for i in control_servers:
        print >> f, i + ',',
    print >> f, '\n'
    print >> f, '[Hosts]'
    print >> f, 'client_servers =',
    for i in client_servers:
        print >> f, i + ',',
    print >> f, '\n'
    print >> f, 'web_servers =',
    for i in web_servers:
        print >> f, i + ',',
    print >> f, '\n'
    print >> f, 'cjdbc_controller =',
    for i in cjdbc_controller:
        print >> f, i + ',',
    print >> f, '\n'
    print >> f, 'database_servers =',
    for i in database_servers:
        print >> f, i + ',',
    f.close()

def main():
    global Heat_template
    global Bottlenecks_repo_dir
    global image_url
    Bottlenecks_repo_dir = "/home/opnfv/bottlenecks"      # same in Dockerfile, docker directory

    image_url = 'http://artifacts.opnfv.org/bottlenecks/rubbos/bottlenecks-trusty-server.img'

    if not (args.conf):
       logger.error("Configuration files are not set for testcase")
       exit(-1)
    else:
       Heat_template = args.conf

    #TO DO:the parameters are all used defaults here, it should be changed depends on what it is really named
    parameters={'image': 'bottlenecks_rubbos_image',
                'key_name': 'bottlenecks_rubbos_keypair',
                'flavor': 'bottlenecks_rubbos_flavor',
                'public_net': os.environ.get('EXTERNAL_NET')}

    print "Heat_template_file: " + Heat_template
    print "parameters:\n" + str(parameters)

    image_created = False
    stack_created = False

    rubbos_env_prepare(Heat_template)
    rubbos_env_cleanup()

    image_created = rubbos_create_images(image_url)
    keyPath = Bottlenecks_repo_dir + "/utils/infra_setup/bottlenecks_key/bottlenecks_key.pub"
    rubbos_create_keypairs(key_path=keyPath)
    rubbos_create_flavors()

    if image_created == True:
        stack_created = rubbos_create_instances(template_file=Heat_template, rubbos_parameters=parameters, stack_name="bottlenecks_rubbos_stack")
    else:
        print "Cannot create instances, as Failed to create image(s)."
        exit (-1)

    rubbos_run()
    rubbos_env_cleanup()

if __name__=='__main__':
    main()
