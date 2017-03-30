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
 b) Automatically generate the testing report for bottlenecks in
different categories.
 c) Implementing Automated Staging.

Scopes of the POSCA testsuite:
 a) Modeling, Testing and Test Result analysis.
 b) Parameters choosing and Algorithms.

Test stories of POSCA testsuite:
 a) Factor test (Stress test): base test cases that Feature test and Optimization will be
dependant on.
 b) Feature test: test cases for features/scenarios.
 c) Optimization test: test to tune the system parameter.

Detailed workflow is illutrated below.

* https://wiki.opnfv.org/display/bottlenecks

Preinstall Packages
====================

* Please refer to release notes.

Run POSCA Locally
=================

POSCA testsuite is hight automated regarding test environment preparation, installing testing tools, excuting tests and show the report/analysis. A few steps are needed to run it locally.

It is presumed that a user is using Compass4nfv to deploy OPNFV Danube and the user login jumper server as root user.

Downloading Bottlenecks Software
--------------------------------

.. code-block:: bash

    git clone https://gerrit.opnfv.org/gerrit/bottlenecks

Preparing Python Virtual Evnironment
------------------------------------

.. code-block:: bash

    . pre_virt_env.sh

Excuting Specified Testcase
---------------------------

Bottlencks provide a CLI interface to run the tests, which is the most convenient way since it is more close to our natural languge. An GUI interface with rest API will also be provided in later update.

.. code-block:: bash

    bottlenecks [testcase run <testcase>] [teststory run <teststory>]

For the *testcase* command, testcase name should be the same as the name of the test case configuration file located in testsuites/posca/testcase_cfg.
For the *teststory* command, a user could specified the test cases to be excuted by defined it in a teststory configuration file located in testsuites/posca/testsuite_story. There is also an example there named *posca_factor_test*.

There are also other 2 ways to run test cases and test stories.
The first one is using shell script.

.. code-block:: bash

    bash run_tests.sh [-h|--help] [-s <test suite>] [-c <test case>]

The second is using python interpreter.

.. code-block:: bash

    python testsuites/posca/run_posca.py [testcase <testcase>] [teststory <teststory>]


Cleaning Up Environment
-----------------------

.. code-block:: bash

    . rm_virt_env.sh


Run POSCA through Community CI
==============================
* POSCA test cases are runned by OPNFV CI now. See https://build.opnfv.org for more information.

Test Result Description
=======================
* Please refer to release notes and also https://wiki.opnfv.org/display/testing/Result+alignment+for+ELK+post-processing
