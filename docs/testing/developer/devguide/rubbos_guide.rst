.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

**********************
Rubbos Testsuite Guide
**********************


Rubbos Introduction
====================
Rubbos is a bulletin board benchmark modeled after an online news forum like Slashdot.
It is an open source Middleware and an n-tier system model which
is used to be deployed on multiple physical node and
to measure the whole performacne of OPNFV platform.
Rubbos can deploy the Apache, tomcat, and DB.
Based on the deployment, rubbos gives the pressure to the whole system.
When the system reaches to the peak, the throughput will not grow more.
This testcase can help to understand the bottlenecks of OPNFV plantform
and improve the performance of OPNFV platform.

Detailed workflow is illutrated below.

.. image:: ../images/Framework_Setup.png
   :width: 770px
   :alt: Bottlenecks Framework Setup

Preinstall Packages
====================
There is a need to install some packages before running the rubbos,
gcc, gettext, g++, libaio1, libaio-dev, make and git are necessary.
When the rubbos runs on the OPNFV community continuous integration(CI)
system, the required packages are installed automately as shown in the
code repository, which is /utils/infra_setup/vm_dev_setup/packages.conf,
besides, the packages can be encapsulated in the images initially.
If someone wants to use rubbos locally, he/she has to install them by
hand, such as in ubuntu 14.04,

.. code-block:: bash

    apt-get update
    apt-get install gettext

How does Rubbos Integrate into Installers
=========================================
1.Community CI System

Rubbos has been successfully integrated into fuel and compass with NOSDN scenario
in OPNFV community CI system.

Heat is used to create 9 instances, which is shown in
/utils/infra_setup/heat_template/HOT_create_instance.sh, the 9 instances are used
for installing Apache, Tomcat, Mysql, Control, Benchmark and 4 Clients. The tools,
such as rubbos, sysstat, oprofile, etc, are installed in these instances to perform
the test, the test results are stored in the Benchmark instance initially, then they
are copied to the Rubbos_result instance, finally, the test results are transferred to
the community dashboard.

There's a need to store our pakages as large as M bytes or G bytes size, such as
the images, jdk, apache-ant, apache-tomcat, etc, the OPNFV community storage system,
Google Cloud Storage, is used, the pakages can be downloaded from
https://artifacts.opnfv.org/bottlenecks/rubbos.

2.Local Deployment

If someone wants to run the rubbos in his own environment, he/she can keep to the following steps,

2.1 Start up instances by using heat, nova or libvert. In Openstack Environemnt,
the heat script can refer /utils/infra_setup/heat_template/HOT_create_instance.sh,
if the openstack doesn't support heat module,
the script /utils/infra_setup/create_instance.sh can be used.
Without Openstack, there's a way to set up instances by using libvert, the scripts are shown under
the directory /utils/rubbos_dev_env_setup.

The image can be downloaded from the community cloud storage

.. code-block:: bash

    curl --connect-timeout 10 -o bottlenecks-trusty-server.img
         http://artifacts.opnfv.org/bottlenecks/rubbos/bottlenecks-trusty-server.img

2.2 Ssh into the control node and clone the bottlenecks codes to the root directory.

.. code-block:: bash

    git clone https://git.opnfv.org/bottlenecks /bottlenecks

2.3 Download the packages and decompress them into the proper directory.

.. code-block:: bash

    curl --connect-timeout 10 -o app_tools.tar.gz
         http://artifacts.opnfv.org/bottlenecks/rubbos/app_tools.tar.gz
    curl --connect-timeout 10 -o rubbosMulini6.tar.gz
         http://artifacts.opnfv.org/bottlenecks/rubbos/rubbosMulini6.tar.gz

.. code-block:: bash

    tar zxf app_tools.tar.gz -C /bottlenecks/rubbos
    tar zxf rubbosMulini6.tar.gz -C /bottlenecks/rubbos/rubbos_scripts

2.4 Ssh into the Control node and run the script

.. code-block:: bash

    source /bottlenecks/rubbos/rubbos_scripts/1-1-1/scripts/run.sh

2.5 Check the test results under the directory /bottlenecks/rubbos/rubbos_results in
Control node. The results are stored in the format of xml,
move them to the brower chrome, then you can see the results.

Test Result Description
=======================
In OPNFV community, the result is shown in the following format

::

   [{'client': 200, 'throughput': 27},
    {'client': 700, 'throughput': 102},
    {'client': 1200, 'throughput': 177},
    {'client': 1700, 'throughput': 252},
    {'client': 2200, 'throughput': 323},
    {'client': 2700, 'throughput': 399},
    {'client': 3200, 'throughput': 473}]

The results are transferred to the community database and a map is drawed on the dashboard.
Along with the growth of the number of the client, the throughput grows at first, then meets
up with a point of inflexion, which is caused by the bottlenecks of the measured system.
