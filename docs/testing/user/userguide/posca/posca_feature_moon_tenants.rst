.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

***********************************************
POSCA feature Test of Moon Security for Tenants
***********************************************

Test Case
=========

+-----------------------------------------------------------------------------+
|Bottlenecks POSCA Soak Test Throughputs                                      |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| posca_feature_moon_tenants                                   |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | Moon authentication capability test for maximum tenants      |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |   /testsuite/posca/testcase_cfg/...                          |
|              |      posca_feature_moon_tenants.yaml                         |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | Max number of tenants                                        |
|              |                                                              |
+--------------+--------------------------------------------------------------+

Configuration
============
::

  load_manager:
    scenarios:
      tool: https request
      # info that the cpus and memes have the same number of data.
      pdp_name: pdp
      policy_name: "MLS Policy example"
      model_name: MLS
      subject_number: 20
      object_number: 20
      timeout: 0.003
      initial_tenants: 0
      steps_tenants: 1
      tolerate_time: 20
      SLA: 5

    runners:
      stack_create: yardstick
      Debug: False
      yardstick_test_dir: "samples"
      yardstick_testcase: "moon_tenant"
