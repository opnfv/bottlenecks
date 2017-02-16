.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

****************************
Project General Test Methods
****************************

For each *test suite*, you can setup *test story* by including several *test cases*
only with one configuration parameter different, by comparing the test results,
you can see the influence of the configuration parameter.

Brahmaputra: rubbos is introduced, which is an end2end NFVI perforamnce tool.
Virtual switch test framework(VSTF) is also introduced,
which is an test framework used for vswitch performance test.

Colorado: rubbos is refactored by using puppet, which makes it quite flexible
to configure with different number of load generator(Client), worker(tomcat).
vstf is refactored by extracting the test case's configuration information.

Danube: posca testsuite is introduced to implementing stress (factor), scenario and 
tuning test in parametric manner. Two testcases are developed and integrated into
community CI pipeline.

***********************************
Test suite & Test case Description
***********************************
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

***********************
Integration Description
***********************
+-------------+----------------------+
| Release     | integrated installer |
+-------------+----------------------+
| Brahmaputra |    Fuel              |
+-------------+----------------------+
| Colorado    |    Compass           |
+-------------+----------------------+
| Danube      |    Compass           |
+-------------+----------------------+