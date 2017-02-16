.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

*********************
Project Testing Guide
*********************

For each *test suite*, you can either setup *test story* or *test case* to run
certain test. *test story* could include several *test cases* as a set in one
configuration file. You could then call the *test story* or *test case* by using
Bottlencks CLI or Python build process.
Details will be shown in the following section.

Brief Introdcution of the Test suites in Project Releases
=============================================================

Brahmaputra: rubbos is introduced, which is an end2end NFVI perforamnce tool.
Virtual switch test framework(VSTF) is also introduced,
which is an test framework used for vswitch performance test.

Colorado: rubbos is refactored by using puppet, which makes it quite flexible
to configure with different number of load generator(Client), worker(tomcat).
vstf is refactored by extracting the test case's configuration information.

Danube: posca testsuite is introduced to implementing stress (factor), scenario and
tuning test in parametric manner. Two testcases are developed and integrated into
community CI pipeline.

Integration Description
=======================
+-------------+----------------------+----------------------+
| Release     | integrated installer | Supported Testsuite  |
+-------------+----------------------+----------------------+
| Brahmaputra |    Fuel              | Rubbos, VSTF         |
+-------------+----------------------+----------------------+
| Colorado    |    Compass           | Rubbos, VSTF         |
+-------------+----------------------+----------------------+
| Danube      |    Compass           | POSCA                |
+-------------+----------------------+----------------------+

Test suite & Test case Description
==================================
+--------+-----------------------------+
|Rubbos  | rubbos_basic                |
|        +-----------------------------+
|        | rubbos_TC1101               |
|        +-----------------------------+
|        | rubbos_TC1201               |
|        +-----------------------------+
|        | rubbos_TC1301               |
|        +-----------------------------+
|        | rubbos_TC1401               |
|        +-----------------------------+
|        | rubbos_heavy_TC1101         |
+--------+-----------------------------+
|vstf    | vstf_Ti1                    |
|        +-----------------------------+
|        | vstf_Ti2                    |
|        +-----------------------------+
|        | vstf_Ti3                    |
|        +-----------------------------+
|        | vstf_Tn1                    |
|        +-----------------------------+
|        | vstf_Tn2                    |
|        +-----------------------------+
|        | vstf_Tu1                    |
|        +-----------------------------+
|        | vstf_Tu2                    |
|        +-----------------------------+
|        | vstf_Tu3                    |
+--------+-----------------------------+
|posca   | posca_stress_ping           |
|        +-----------------------------+
|        | posca_stress_traffic        |
|        |(posca_factor_sys_bandwidth) |
+--------+-----------------------------+

Installation of Testsuites
==========================

* TODO

Setting Up Configrations
========================

* TODO

Run Tests Brief
===============

* TODO
* More will be shown in the platform overview
