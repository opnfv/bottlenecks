.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

***************************************************
POSCA Stress (Factor) Test of Multistack Storage
***************************************************

Test Case
========

+--------------------------------------------------------------------------------------+
|Bottlenecks POSCA Stress Test MultiStack Storage                                      |
|                                                                                      |
+--------------+-----------------------------------------------------------------------+
|test case name| posca_factor_multistack_storage                                       |
|              |                                                                       |
+--------------+-----------------------------------------------------------------------+
|description   | Stress test regarding multistack storage using                        |
|              | yardstick as a runner                                                 |
+--------------+-----------------------------------------------------------------------+
|configuration | config file:                                                          |
|              |   /testsuite/posca/testcase_cfg/posca_factor_multistack_storage.yaml  |
|              |                                                                       |
|              | stack number: 5, 10, 20, 50 ...                                       |
|              |                                                                       |
+--------------+-----------------------------------------------------------------------+
|test result   | Read / Write IOPS, Throughput, latency                                |
|              |                                                                       |
+--------------+-----------------------------------------------------------------------+

Configuration
============
::

    load_manager:
      scenarios:
        tool: fio
        test_times: 10
        rw: write, read, rw, rr, randomrw
        bs: 4k
        size: 50g
        rwmixwrite: 50
        num_stack: 1, 3
        volume_num: 1
        numjobs: 1
        direct: 1

      contexts:
        stack_create: yardstick
        flavor:
        yardstick_test_ip:
        yardstick_test_dir: "samples"
        yardstick_testcase: "storage_bottlenecks"

    dashboard:
      dashboard: "y"
      dashboard_ip:
