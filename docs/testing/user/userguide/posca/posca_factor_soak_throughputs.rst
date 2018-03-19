.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

*************************************
POSCA Factor Test of Soak Throughputs
*************************************

Test Case
========

+-----------------------------------------------------------------------------+
|Bottlenecks POSCA Soak Test Throughputs                                      |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| posca_factor_soak_throughputs                                |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | Long duration stability tests of data-plane traffic          |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |   /testsuite/posca/testcase_cfg/...                          |
|              |      posca_factor_soak_throughputs.yaml                      |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | THROUGHPUT,THROUGHPUT_UNITS,MEAN_LATENCY,LOCAL_CPU_UTIL,     |
|              | REMOTE_CPU_UTIL,LOCAL_BYTES_SENT,REMOTE_BYTES_RECVD          |
+--------------+--------------------------------------------------------------+

Configuration
============
::

  load_manager:
    scenarios:
      tool: netperf
      test_duration_hours: 1
      vim_pair_ttl: 300
      vim_pair_lazy_cre_delay: 2
      package_size:
      threshhold:
          package_loss: 0%
          latency: 300

    runners:
      stack_create: yardstick
      flavor:
      yardstick_test_dir: "samples"
      yardstick_testcase: "netperf_soak"
