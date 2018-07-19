.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

****************************
Testing-scheduler User Guide
****************************


Testing-scheduler Introduction
==============================

Testing scheduler aims to schedule the testing process on NFV(Network 
Function Virtualizaion) platform or MSA(Microservice Architecture) 
application.By creating a testcase, you can implements a testing 
process integrates and schedules the other testing frameworks and tools.
You can also create a testsuite which contains several testcases, and run
all the testcases at a time.


Preinstall Packages
===================

* Docker: https://docs.docker.com/engine/installation/
    * For Ubuntu, please refer to https://docs.docker.com/engine/installation/linux/ubuntu/

* Docker-Compose: https://docs.docker.com/compose/

.. code-block:: bash

    if [ -d usr/local/bin/docker-compose ]; then
        rm -rf usr/local/bin/docker-compose
    fi
    curl -L https://github.com/docker/compose/releases/download/1.11.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose


Run Testing-scheduler
=====================

There are a few steps to do.


Download Bottlenecks Software
-----------------------------

.. code-block:: bash

    mkdir -p /some/dir
    git clone https://gerrit.opnfv.org/gerrit/bottlenecks
    cd bottlenecks/testing-scheduler


Build And Run Docker Containers
-------------------------------

.. code-block:: bash

    cd docker
    sh build.sh
    sh run.sh


build.sh is used to build the images, and run.sh is use to 
run the containers based on the images.
If you are not the root user, you need to use 'sudo', like:

.. code-block:: bash

    cd docker
    sudo sh build.sh
    sudo sh run.sh


Otherwise there will be a problem of "Permission Denied".
The second command takes approximately 1h to finish(
so need some patience :) ), and the latter one just takes a few minutes.

You can use command the check whether all the containers are in running.

.. code-block:: bash

    docker ps

if the output contains 6 containers as below, then the project 
runs successfully:

* t-scheduler-server
* t-scheduler-ui
* conductor_conductor-server_1
* conductor_conductor-ui_1
* conductor_dynomite_1
* conductor_elasticsearch_1

Sometimes, the command execution fails, and you need to read the sections:
*(Optional)Commands Explanation* , 
*(Optional) Build And Run Containers Seperately* to solve it.


Start To Use Via Web
--------------------
You can visit the web pages via the url: http://your-host-ip:5311/.

You can do these operations:

* test suite CRUD
* test case CRUD
* execute a single test case
* execute several chosen test cases
* execute a single test suite
* test service CRUD
* context setting

Cleaning Up Environment
-----------------------

.. code-block:: bash

    cd docker
    sh clean.sh


(Optional)Commands Explanation
------------------------------

The directory(**docker**) contains the shell scripts which are used 
to build this project(**testing-scheduler**) as a dockerized application.
Built by these scripts, the dockerized application will contain 
6 containers(1 + 1 + 4). They can be divided as three components:

* 1 server container: server component of **testing-scheduler**.
* 1 webUI container: ui component of **testing-scheduler**.
* a group of 4 containers of Conductor.

Correspondingly, there are three subdirectories in the current 
directory(**docker**):

* server: contains scirpts of running server container.
* ui: contains scirpts of running ui container.
* plugin:  contains scirpts of running Conductor containers.

The three subdirectories contains scripts respectively.The scripts 
(in one subdirectory) are used to build image and start container 
for the single component.

Essentially,  the **build.sh**  and **run.sh** (in the directory(**docker**)) 
call the subdirectory scripts to build all three components.


(Optional) Build And Run Containers Seperately
----------------------------------------------

If you run the containers successfully, you can skip this section.
As said in *Build And Run Docker Containers*, build step will need about 1h to 
finish.But it sometime will failed due to the network, and the rebuild will 
take a great time cost.So we can build and run the containers seperately 
according to the three subdirectories(**server**, **ui**, **plugin**).The 
steps are similar to *Build And Run Docker Containers*.

*IMPORTANT: There are relationships in these components(some need to be 
created before other).So you can only build the components below in the 
order:* **plugin** -> **server** -> **ui** .

* enter the subdirectory(**$dir** stands for **server**, **ui**, **plugin**).

.. code-block:: bash

    cd $dir

* build the docker images.

.. code-block:: bash

    sh build.sh

* run the docker containers.

.. code-block:: bash

    sh run.sh