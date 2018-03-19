.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

************************************************************
POSCA feature Test of Moon Security for resources per tenant
************************************************************

Test Case
=========

+-----------------------------------------------------------------------------+
|Bottlenecks POSCA Soak Test Throughputs                                      |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| posca_feature_moon_resources                                 |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | Moon authentication capability test for maximum number of    |
|              | authentication operations per tenant                         |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |   /testsuite/posca/testcase_cfg/...                          |
|              |      posca_feature_moon_resources.yaml                       |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | number of tenants, max number of users                       |
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
      tenants: 1,5,10,20
      subject_number: 10
      object_number: 10
      timeout: 0.2

    runners:
      stack_create: yardstick
      Debug: False
      yardstick_test_dir: "samples"
      yardstick_testcase: "moon_resource"
