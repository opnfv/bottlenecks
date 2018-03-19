.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

***************************************************
POSCA Stress Test of Storage Usage
***************************************************

Test Case
========

+-----------------------------------------------------------------------------+
|Bottlenecks POSCA Stress Test Storage                                        |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| posca_factor_storperf                                        |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | Stress test regarding storage using Storperf                 |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |   /testsuite/posca/testcase_cfg/posca_posca_storperf.yaml    |
|              |                                                              |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | Read / Write IOPS, Throughput, latency                       |
|              |                                                              |
+--------------+--------------------------------------------------------------+

Configuration
============
::

    load_manager:
      scenarios:
        tool: storperf
