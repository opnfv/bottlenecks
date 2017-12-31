.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

**********
User Guide
**********

For each *testsuite*, you can either setup *teststory* or *testcase* to run
certain test. *teststory* comprises several *testcases* as a set in one
configuration file. You could call *teststory* or *testcase* by using
Bottlenecks user interfaces.
Details will be shown in the following section.

Brief Introdcution of the Test suites in Project Releases
=============================================================

Brahmaputra:

* rubbos is introduced, which is an end2end NFVI perforamnce tool.
* Virtual switch test framework (VSTF) is also introduced, which is an test framework used for vswitch performance test.

Colorado:

* rubbos is refactored by using puppet, and ease the integration with several load generators(Client) and worker(Tomcat).
* VSTF is refactored by extracting the test case's configuration information.

Danube:

* posca testsuite is introduced to implement stress (factor), feature and tuning test in parametric manner.
* Two testcases are developed and integrated into community CI pipeline.
* Rubbos and VSTF are not supported any more.

Euphrates:

* Introduction of a simple monitoring module, i.e., Prometheus+Collectd+Node+Grafana to monitor the system behavior when executing stress tests.
* Support VNF scale up/out tests to verify NFVI capability to adapt the resource consuming.
* Extend Life-cycle test to data-plane to validate the system capability to handle concurrent networks usage.
* Testing framework is revised to support installer-agnostic testing.

These enhancements and test cases help the end users to gain more comprehensive understanding of the SUT.
Graphic reports of the system behavior additional to test cases are provided to indicate the confidence level of SUT.
Installer-agnostic testing framework allow end user to do stress testing adaptively over either Open Source or commercial deployments.

Integration Description
=======================
+-------------+----------------------+----------------------+
| Release     | Integrated Installer | Supported Testsuite  |
+-------------+----------------------+----------------------+
| Brahmaputra |    Fuel              | Rubbos, VSTF         |
+-------------+----------------------+----------------------+
| Colorado    |    Compass           | Rubbos, VSTF         |
+-------------+----------------------+----------------------+
| Danube      |    Compass           | POSCA                |
+-------------+----------------------+----------------------+
| Euphrates   |    Any               | POSCA                |
+-------------+----------------------+----------------------+

Test suite & Test case Description
==================================
+--------+-------------------------------------+
|POSCA   | posca_factor_ping                   |
|        +-------------------------------------+
|        | posca_factor_system_bandwidth       |
|        +-------------------------------------+
|        | posca_facotor_soak_througputs       |
|        +-------------------------------------+
|        | posca_feature_vnf_scale_up          |
|        +-------------------------------------+
|        | posca_feature_vnf_scale_out         |
|        +-------------------------------------+
|        | posca_factor_storperf               |
|        +-------------------------------------+
|        | posca_factor_storage                |
|        +-------------------------------------+
|        | posca_factor_multistack_storage     |
+--------+-------------------------------------+

As for the abandoned test suite in the previous Bottlenecks releases, please
refer to http://docs.opnfv.org/en/stable-danube/submodules/bottlenecks/docs/testing/user/userguide/deprecated.html.
