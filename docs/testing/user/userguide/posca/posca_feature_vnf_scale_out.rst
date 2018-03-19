.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

***********************************
POSCA feature Test of VNF Scale Out
***********************************

Test Case
=========

+-----------------------------------------------------------------------------+
|Bottlenecks POSCA Soak Test Throughputs                                      |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| posca_feature_nfv_scale_out                                  |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | SampleVNF Scale Out Test                                     |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |   /testsuite/posca/testcase_cfg/...                          |
|              |      posca_feature_nfv_scale_out.yaml                        |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | throughputs, latency, loss rate                              |
|              |                                                              |
+--------------+--------------------------------------------------------------+

Configuration
============
::

  load_manager:
    scenarios:
      number_vnfs: 1, 2, 4
      iterations: 10
      interval: 35

    runners:
      stack_create: yardstick
      flavor:
      yardstick_test_dir: "samples/vnf_samples/nsut/acl"
      yardstick_testcase: "tc_heat_rfc2544_ipv4_1rule_1flow_64B_trex_correlated_traffic_scale_out"
