.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

*********************
POSCA Testsuite Guide
*********************


POSCA Introduction
====================
The POSCA (Parametric Bottlenecks Testing Catalogue) testsuite
classifies the bottlenecks test cases and results into 5 categories.
Then the results will be analyzed and bottlenecks will be searched
among these categories.

The POSCA testsuite aims to locate the bottlenecks in parmetric
manner and to decouple the bottlenecks regarding the deployment
requirements.
The POSCA testsuite provides an user friendly way to profile and
understand the E2E system behavior and deployment requirements.

Goals of the POSCA testsuite:
 a) Automatically locate the bottlenecks in a iterative manner.
 b) Automatically generate the testing report for bottlenecks in different categories.
 c) Implementing Automated Staging.

Scopes of the POSCA testsuite:
 a) Modeling, Testing and Test Result analysis.
 b) Parameters choosing and Algorithms.

Test stories of POSCA testsuite:
 a) Factor test (Stress test): base test cases that Feature test and Optimization will be dependant on.
 b) Feature test: test cases for features/scenarios.
 c) Optimization test: test to tune the system parameter.

Detailed workflow is illutrated below.

* https://wiki.opnfv.org/display/bottlenecks


Preinstall Packages
====================

* Docker: https://docs.docker.com/engine/installation/
    * For Ubuntu, please refer to https://docs.docker.com/engine/installation/linux/ubuntu/

* Docker-Compose: https://docs.docker.com/compose/

.. code-block:: bash

    if [ -d usr/local/bin/docker-compose ]; then
        rm -rf usr/local/bin/docker-compose
    fi
    curl -L https://github.com/docker/compose/releases/download/1.11.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose


Run POSCA Locally
=================

POSCA testsuite is highly automated regarding test environment preparation, installing testing tools, excuting tests and showing the report/analysis.
A few steps are needed to run it locally.

In Euratphtes, Bottlenecks has modified its framework to support installer-agnostic testing which means that test cases could executed over different deployments.


Downloading Bottlenecks Software
--------------------------------

.. code-block:: bash

    mkdir /home/opnfv
    cd /home/opnfv
    git clone https://gerrit.opnfv.org/gerrit/bottlenecks
    cd bottlenecks


Preparing Python Virtual Evnironment
------------------------------------

.. code-block:: bash

    . pre_virt_env.sh


Preparing configuration/description files
-----------------------------------------

Put OpenStack RC file (admin_rc.sh), os_carcert and pod.yaml (pod descrition file) in /tmp directory.
Write the following command in admin_rc.sh

.. code-block:: bash

    export OS_CACERT=/tmp/os_cacert

If you are using compass, fuel, apex or joid to deploy your openstack environment, you could uses the following command to get the required files.

.. code-block:: bash

    bash /utils/env_prepare/config_prepare.sh -i <installer> [--debug]


Executing Specified Testcase
---------------------------

Bottlencks provide a CLI interface to run the tests, which is one of the most convenient way since it is more close to our natural languge. An GUI interface with rest API will also be provided in later update.

.. code-block:: bash

    bottlenecks testcase|teststory run <testname>

For the *testcase* command, testname should be as the same name of the test case configuration file located in testsuites/posca/testcase_cfg.
For stress tests in Danube/Euphrates, *testcase* should be replaced by either *posca_factor_ping* or *posca_factor_system_bandwidth*.
For the *teststory* command, a user could specified the test cases to be excuted by defined it in a teststory configuration file located in testsuites/posca/testsuite_story. There is also an example there named *posca_factor_test*.

There are also other 2 ways to run test cases and test stories.
The first one is using shell script.

.. code-block:: bash

    bash run_tests.sh [-h|--help] -s <testsuite>|-c <testcase>

The second is using python interpreter.

.. code-block:: bash

    $REPORT=False
    opts="--privileged=true -id"
    docker_volume="-v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp"
    docker run $opts --name bottlenecks-load-master $docker_volume opnfv/bottlenecks:latest /bin/bash
    sleep 5
    POSCA_SCRIPT="/home/opnfv/bottlenecks/testsuites/posca"
    docker exec bottlenecks-load-master python ${POSCA_SCRIPT}/../run_posca.py testcase|teststory <testname> ${REPORT}


Showing Report
--------------

Bottlenecks uses ELK to illustrate the testing results.
Asumming IP of the SUT (System Under Test) is denoted as ipaddr,
then the address of Kibana is http://[ipaddr]:5601. One can visit this address to see the illustrations.
Address for elasticsearch is http://[ipaddr]:9200. One can use any Rest Tool to visit the testing data stored in elasticsearch.

Cleaning Up Environment
-----------------------

.. code-block:: bash

    . rm_virt_env.sh


If you want to clean the dockers that established during the test, you can excute the additional commands below.

.. code-block:: bash

    bash run_tests.sh --cleanup

Note that you can also add cleanup parameter when you run a test case. Then environment will be automatically cleaned up when
completing the test.

Run POSCA through Community CI
==============================
POSCA test cases are runned by OPNFV CI now. See https://build.opnfv.org for details of the building jobs.
Each building job is set up to execute a single test case. The test results/logs will be printed on the web page and
reported automatically to community MongoDB. There are two ways to report the results.

1. Report testing result by shell script

.. code-block:: bash

    bash run_tests.sh [-h|--help] -s <testsuite>|-c <testcase> --report

2. Report testing result by python interpreter

.. code-block:: bash

    REPORT=True
    opts="--privileged=true -id"
    docker_volume="-v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp"
    docker run $opts --name bottlenecks-load-master $docker_volume opnfv/bottlenecks:latest /bin/bash
    sleep 5
    REPORT="True"
    POSCA_SCRIPT="/home/opnfv/bottlenecks/testsuites/posca"
    docker exec bottlenecks_bottlenecks_1 python ${POSCA_SCRIPT}/run_posca.py testcase|teststory <testcase> ${REPORT}

Test Result Description
=======================
* Please refer to release notes and also https://wiki.opnfv.org/display/testing/Result+alignment+for+ELK+post-processing
