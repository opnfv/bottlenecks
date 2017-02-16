.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Tech and others.

**********************************************
POSCA Stress (Factor) Test of System bandwidth
**********************************************


Test Case
========
+-----------------------------------------------------------------------------+
|Bottlenecks POSCA Stress Test Traffic                                        |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| posca_stress_ping                                            |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | Stress test regarding baseline of the system for a single    |
|              | user, i.e., a VM pair while increasing the package size      |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |   /testsuite/posca/testcase_cfg/posca_factor_system_bandwith |
|              |                                                              |
|              | stack number: 1                                              |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | PKT loss rate, latency, throupht, cpu usage                  |
|              |                                                              |
+--------------+--------------------------------------------------------------+

Configration
===========
test_config:
  tool: netperf
  protocol: tcp
  test_time: 20
  tx_pkt_sizes: 64, 256, 1024, 4096, 8192, 16384, 32768, 65536
  rx_pkt_sizes: 64, 256, 1024, 4096, 8192, 16384, 32768, 65536
  cpu_load: 0.9
  latency: 100000
runner_config:
  dashboard: "y"
  dashboard_ip:
  stack_create: yardstick
  yardstick_test_ip:
  yardstick_test_dir: "samples"
  yardstick_testcase: "netperf_bottlenecks"
  