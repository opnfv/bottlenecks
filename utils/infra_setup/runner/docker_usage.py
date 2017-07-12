#!/usr/bin/env python
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
'''This file contain all function about yardstick API.
At present, This file contain the following function:
1.Ask Yardstick to run testcase and get a task id.
2.use task id to ask yardstick for data.
3.Ask yardstick for InfluxDB create
4.how the process of task.'''

import docker

yardstick_info = None
ELK_info = None


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
        yardstick_info["containner"] = env_docker
        yardstick_info["ip"] = get_docker_ip(docker_name)
        return env_docker
    except docker.errors.NotFound:
        pass
    env_docker = client.containers.run(image="opnfv/yardstick:latest",
                                       privileged=True,
                                       detach=True,
                                       ports={'8888': '5000'},
                                       volumes={'/var/run/docker.sock':
                                                '/var/run/docker.sock'},
                                       name=docker_name)
    yardstick_info["containner"] = env_docker
    yardstick_info["ip"] = get_docker_ip(docker_name)
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
    ip_address = client.inspect_container(env_docker.id)
    return ip_address


def docker_exec_cmd(docker, cmd):
    return docker.exec_cmd(cmd)


def remove_docker(docker_name):
    docker = docker_find(docker_name)
    docker.kill()
    docker.remove()

