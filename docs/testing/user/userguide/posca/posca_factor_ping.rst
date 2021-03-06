.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

***************************************************
POSCA Stress (Factor) Test of Perfomance Life-Cycle
***************************************************

Test Case
========

+-----------------------------------------------------------------------------+
|Bottlenecks POSCA Stress Test Ping                                           |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| posca_posca_ping                                             |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | Stress test regarding life-cycle while using ping            |
|              | to validate the VM pairs constructions                       |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |   /testsuite/posca/testcase_cfg/posca_posca_ping.yaml        |
|              |                                                              |
|              | stack number: 5, 10, 20, 50 ...                              |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | PKT loss rate, success rate, test time, latency              |
|              |                                                              |
+--------------+--------------------------------------------------------------+

Configuration
============
::

    load_manager:
      scenarios:
        tool: ping
        test_times: 100
        package_size:
        num_stack: 5, 5
        package_loss: 0

      contexts:
        stack_create: yardstick
        flavor:
        yardstick_test_ip:
        yardstick_test_dir: "samples"
        yardstick_testcase: "ping_bottlenecks"

    dashboard:
      dashboard: "y"
      dashboard_ip:
