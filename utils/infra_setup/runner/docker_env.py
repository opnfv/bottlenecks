#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file contain some function about docker API.
At present, This file contain the following function:
1.Ask Docker service to create a docker(yardstick or ELK).
2.get a docker ip.
3.Remove a docker.'''

import docker
import os
import socket

yardstick_info = {}
ELK_info = {}
storperf_info = {}


def get_client():
    client = docker.from_env()
    return client


def docker_find(docker_name):
    client = get_client()
    docker_client = client.containers.get(docker_name)
    return docker_client


def env_yardstick(docker_name):
    client = get_client()
    yardstick_info["name"] = docker_name
    try:
        env_docker = docker_find(docker_name)
        yardstick_info["container"] = env_docker
        yardstick_info["ip"] = get_docker_ip(docker_name)
        return env_docker
    except docker.errors.NotFound:
        pass
    volume = get_self_volume()
    yardstick_tag = os.getenv("Yardstick_TAG")
    if yardstick_tag is None:
        yardstick_tag = "danube.3.1"
    env_docker = client.containers.run(image="opnfv/yardstick:%s"
                                             % yardstick_tag,
                                       privileged=True,
                                       tty=True,
                                       detach=True,
                                       ports={'5000': '8888'},
                                       volumes=volume,
                                       name=docker_name)
    yardstick_info["container"] = env_docker
    yardstick_info["ip"] = get_docker_ip(docker_name)
    return env_docker


def env_storperf(docker_name):
    client = get_client()
    storperf_info["name"] = docker_name
    try:
        env_docker = docker_find(docker_name)
        storperf_info["container"] = env_docker
        storperf_info["ip"] = get_docker_ip(docker_name)
        return env_docker
    except docker.errors.NotFound:
        pass
    volume = get_self_volume()
    env_docker = client.containers.run(image="opnfv/storperf:latest"
                                       privileged=True,
                                       tty=True,
                                       detach=True,
                                       ports={'5000': '5011',
                                              '8000': '8011'},
                                       volumes=volume,
                                       name=docker_name)
    storperf_info["container"] = env_docker
    storperf_info["ip"] = get_docker_ip(docker_name)
    return env_docker


def env_bottlenecks(docker_name):
    client = get_client()
    volume = get_self_volume()
    env_docker = client.containers.run(image="opnfv/bottlenecks:latest",
                                       privileged=True,
                                       detach=True,
                                       ports={'8888': '5000'},
                                       volumes=volume,
                                       name=docker_name)
    return env_docker


def env_elk(docker_name):
    client = get_client()
    ELK_info["name"] = docker_name
    try:
        env_docker = docker_find(docker_name)
        ELK_info["container"] = env_docker
        ELK_info["ip"] = get_docker_ip(docker_name)
        return env_docker
    except docker.errors.NotFound:
        pass
    env_docker = client.containers.run(image="sebp/elk:es241_l240_k461",
                                       privileged=True,
                                       detach=True,
                                       ports={'5044': '5044',
                                              '5601': '5601',
                                              '9200': '9200'},
                                       name=docker_name)
    ELK_info["container"] = env_docker
    ELK_info["ip"] = get_docker_ip(docker_name)
    return env_docker


def get_docker_ip(docker_name):
    env_docker = docker_find(docker_name)
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    docker_inspect = client.inspect_container(env_docker.id)
    ip_address = docker_inspect["NetworkSettings"]["IPAddress"]
    return ip_address


def docker_exec_cmd(docker, cmd):
    return docker.exec_run(cmd)


def get_self_volume():
    self_volume = {}
    hostname = socket.gethostname()
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    volume = client.inspect_container(hostname)["Mounts"]
    for i in volume:
        self_volume[i['Source']] = i['Destination']
    return self_volume


def remove_docker(docker_name):
    docker = docker_find(docker_name)
    docker.kill()
    docker.remove()
