.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.


==========================================
OPNFV Danube Release Notes for Bottlenecks
==========================================

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
| Feb 17nd, 2016 |  1.1               | Bottlenecks Danube release 1.0  |
|                |                    |                                 |
+----------------+--------------------+---------------------------------+


Summary
=======

* Documentation generated with Sphinx

  * User guide

  * Installation Procedure

  * Release Notes (this document)

  * Platform Overview

  * Configuration Guide

* Bottlenecks test suite

  * Jenkins Jobs for OPNFV community labs

* Bottlenecks framework

* Bottlenecks test cases

The *Bottlenecks software* is developed in the OPNFV community, by the
Bottlenecks_ team.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | Bottlenecks                          |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/tag**                         | Bottlenecks/brahmaputra.1.0          |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Bottlenecks Docker image tag**     | brahmaputra.1.0                      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Brahmaputra base release             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | February 25 2016                     |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | Brahmaputra base release             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

+--------------------------------------+--------------------------------------+
| **Project**                          | Bottlenecks                          |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/tag**                         | Bottlenecks/colorado.1.0             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Bottlenecks Docker image tag**     | colorado.1.0                         |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Colorado base release                |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | September 22 2016                    |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | Colorado base release                |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Danube Deliverables
===================

Software Deliverables
---------------------

**Bottlenecks source code <danube.1.0>**

* https://gerrit.opnfv.org/gerrit/gitweb?p=bottlenecks.git;a=summary


Documentatiion Deliverables
---------------------------

**Bottlenecks documentation <danube.1.0>**

* Platformation Overview: http://artifacts.opnfv.org/bottlenecks/danube/1.0/docs/platformoverview/index.html
* Configuration Guide: http://artifacts.opnfv.org/bottlenecks/danube/1.0/configurationguide/index.html
* Installation Guide: http://artifacts.opnfv.org/bottlenecks/danube/docs/installationprocedure/index.html
* http://artifacts.opnfv.org/bottlenecks/danube/1.0/releasenotes/index.html
* User Guide: http://artifacts.opnfv.org/bottlenecks/danube/1.0/docs/userguide/index.html

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

* In Danube, POSCA testsuite is introduced and two stress tests are implemented.
* In Colorado, rubbos is refactored by using puppet, which makes it quite flexible
to configure with different number of load generator(Client), worker(tomcat).
* In Colorado, vstf is refactored by extracting the test case's configuration information.


Known restrictions/issues
=========================

* TODO


Test results
============

Test results are available in:

 - jenkins logs on CI: https://build.opnfv.org/ci/view/bottlenecks/


Open JIRA tickets
=================

+------------------+-----------------------------------------------+
|   JIRA           |         Description                           |
+==================+===============================================+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+


Useful links
============

 - WIKI project page: https://wiki.opnfv.org/display/Bottlenecks

 - Bottlenecks jira page: https://jira.opnfv.org/projects/BOTTLENECK/issues/

 - Bottlenecks repo: https://git.opnfv.org/cgit/bottlenecks/

 - Bottlenecks CI dashboard: https://build.opnfv.org/ci/view/bottlenecks

 - Bottlenecks IRC chanel: #opnfv-bottlenecks


