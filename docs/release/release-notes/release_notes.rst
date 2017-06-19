.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.


==================================================
Bottlenecks Release Notes for OPNFV Danube Release
==================================================

.. _Bottlenecks: https://wiki.opnfv.org/display/bottlenecks


Abstract
========

This document describes the release notes of Bottlenecks project.


License
=======

OPNFV release notes for Bottlenecks Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

The *Bottlenecks software* is opensource software, licensed under the terms of the
Apache License, Version 2.0.


Version History
===============

+----------------+--------------------+---------------------------------+
| *Date*         | *Version*          | *Comment*                       |
|                |                    |                                 |
+----------------+--------------------+---------------------------------+
| Sept 22nd, 2016|  1.0               | Bottlenecks Colorado release 1.0|
|                |                    |                                 |
+----------------+--------------------+---------------------------------+
| Feb 17nd, 2017 |  1.1               | Bottlenecks Danube release 1.0  |
|                |                    |                                 |
+----------------+--------------------+---------------------------------+
| Mar 24nd, 2017 |  1.2               | Bottlenecks Danube release 1.0  |
|                |                    |                                 |
+----------------+--------------------+---------------------------------+
| Mar 24nd, 2017 |  1.3               | Bottlenecks Danube release 1.0  |
|                |                    |                                 |
+----------------+--------------------+---------------------------------+
| Apr 25th, 2017 |  1.4               | Bottlenecks Danube release 2.0  |
|                |                    |                                 |
+----------------+--------------------+---------------------------------+
| Jun 19th, 2017 |  1.5               | Bottlenecks Danube release 3.0  |
|                |                    |                                 |
+----------------+--------------------+---------------------------------+

Summary
=======

* Documentation generated with Sphinx

  * Release

    * Release Notes

  * Testing

    * User Guide

    * Development Guide

The *Bottlenecks software* is developed in the OPNFV community, by the
Bottlenecks_ team.

Release Data
============

Danube Release Data
-----------------------

+--------------------------------------+--------------------------------+
| **Project**                          | Bottlenecks                    |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Repo/tag**                         | * Bottlenecks/danube.1.0       |
|                                      | * Bottlenecks/danube.2.0       |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Bottlenecks Docker image tag**     | * danube.1.0                   |
|                                      | * danube.2.0                   |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Release designation**              | * Danube 1.0                   |
|                                      | * Danube 2.0                   |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Release date**                     | * March 31st 2017              |
|                                      | * May 1st 2017                 |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Purpose of the delivery**          | Danube stable release          |
|                                      |                                |
+--------------------------------------+--------------------------------+

Colorado Release Data
-----------------------

+--------------------------------------+--------------------------------+
| **Project**                          | Bottlenecks                    |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Repo/tag**                         | Bottlenecks/colorado.1.0       |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Bottlenecks Docker image tag**     | * colorado.1.0                 |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Release designation**              | * Colorado 1.0                 |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Release date**                     | * September 22 2016            |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Purpose of the delivery**          | Colorado stable release        |
|                                      |                                |
+--------------------------------------+--------------------------------+

Bramaputra Release Data
-----------------------

+--------------------------------------+--------------------------------+
| **Project**                          | Bottlenecks                    |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Repo/tag**                         | Bottlenecks/brahmaputra.1.0    |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Bottlenecks Docker image tag**     | * brahmaputra.1.0              |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Release designation**              | * Brahmaputra 1.0              |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Release date**                     | * February 25 2016             |
|                                      |                                |
+--------------------------------------+--------------------------------+
| **Purpose of the delivery**          | Brahmaputra stable release     |
|                                      |                                |
+--------------------------------------+--------------------------------+


Danube Deliverables
===================

Software Deliverables
---------------------

**Bottlenecks source code <danube>**

* https://gerrit.opnfv.org/gerrit/gitweb?p=bottlenecks.git;a=summary


Documentatiion Deliverables
---------------------------

**Bottlenecks documentation <danube>**

* Release Notes: http://docs.opnfv.org/en/stable-danube/submodules/bottlenecks/docs/release/release-notes/release_notes.html
* User Guide: http://docs.opnfv.org/en/stable-danube/submodules/bottlenecks/docs/testing/user/userguide/index.html
* Development Guide: http://docs.opnfv.org/en/stable-danube/submodules/bottlenecks/docs/testing/developer/devguide/index.html

Colorado Deliverables
=====================

Software Deliverables
---------------------

**Bottlenecks source code <colorado.1.0>**

* https://gerrit.opnfv.org/gerrit/gitweb?p=bottlenecks.git;a=summary


Documentatiion Deliverables
---------------------------

**Bottlenecks documentation <colorado.1.0>**

* Platformation Overview: http://artifacts.opnfv.org/bottlenecks/colorado/1.0/docs/platformoverview/index.html
* Configuration Guide: http://artifacts.opnfv.org/bottlenecks/colorado/1.0/configurationguide/index.html
* Installation Guide: http://artifacts.opnfv.org/bottlenecks/colorado/docs/installationprocedure/index.html
* http://artifacts.opnfv.org/bottlenecks/colorado/1.0/releasenotes/index.html
* User Guide: http://artifacts.opnfv.org/bottlenecks/colorado/1.0/docs/userguide/index.html

Reason for Version
==================

* In Danube, POSCA testsuite is introduced and two stress tests are implemented. Rubbos and vstf are
not supported in this release. Their documentations for former releases will only be kept this release.
* In Colorado, rubbos is refactored by using puppet, which makes it quite flexible to configure with different number of load generator(Client), worker(tomcat).
* In Colorado, vstf is refactored by extracting the test case's configuration information.


Known restrictions/issues
=========================

* In Danube, Bottlenecks use Yardstick to do stress tests by iteratively calling yardstick running test cases and in the meantime increasing load.

  * Sometimes, Yardstick just waits for the test environment preparing.
  This cause troubles since it seams to get Yardstick into a loop to keep waiting.
  For OPNFV CI, this loop will be automatically stopped because of the default timeout setting. However, for local testing, user should stop this loop manually.

  * Sometimes, Yardstick will return empty test results with test flag indicating test is excuted succefully.
  It maybe because of the environment issue or poor internet connection causing testing tools are not installed successfully.

* Sometimes, a process will go to dormancy. In this case, if a tool is installed in the SUT and its process go dormancy, we try to call it twice. Normally, it will response.


Test results
============

Test results are available in:

 - jenkins logs on CI: https://build.opnfv.org/ci/view/bottlenecks/

The test results are reported to MongoDB. An example is given below.

::

    {
      "project_name": "bottlenecks",
      "scenario": "os-odl_l2-nofeature-ha",
      "stop_date": null,
      "trust_indicator": null,
      "case_name": "posca_stress_ping",
      "build_tag": "bottlenecks-compass-posca_stress_ping-baremetal-daily-master",
      "version": "master",
      "pod_name": "huawei-pod2",
      "criteria": "PASS",
      "installer": "compass",
      "_id": "58cf4d3e32c829000a1150a8",
      "start_date": "2017-3-9 4:33:04",
      "details": {}
    }

For more information, please refer to: https://wiki.opnfv.org/display/testing/Result+alignment+for+ELK+post-processing
 - Results reported in MongoDB could find at http://testresults.opnfv.org/test/api/v1/results?project=bottlenecks
 - Test Cases are defined in http://testresults.opnfv.org/test/api/v1/results?project=bottlenecks

Open JIRA tickets
=================

+------------------+----------------------------------------------------+
|   JIRA           |         Description                                |
+==================+====================================================+
| BOTTLENECK-103   | Refactoring the Bottlenecks tesing workflow        |
+------------------+----------------------------------------------------+
| BOTTLENECK-147   | Investigting why calling remote docker client      |
+------------------+----------------------------------------------------+


Useful links
============

 - WIKI project page: https://wiki.opnfv.org/display/Bottlenecks

 - Bottlenecks jira page: https://jira.opnfv.org/projects/BOTTLENECK/issues/

 - Bottlenecks repo: https://git.opnfv.org/cgit/bottlenecks/

 - Bottlenecks CI dashboard: https://build.opnfv.org/ci/view/bottlenecks

 - Bottlenecks IRC chanel: #opnfv-bottlenecks
