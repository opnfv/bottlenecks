.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

*********************
POSCA Testsuite Guide
*********************


POSCA Introduction
====================
The POSCA (Parametric Bottlenecks Testing Catalogue) testsuite
classifies the bottlenecks test cases and results into 5 categories.
Then the results will be analyzed and bottlenecks will be searched
among these categories.

The POSCA testsuite aims to locate the bottlenecks in parmetric
manner and to decouple the bottlenecks regarding the deployment
requirements.
The POSCA testsuite provides an user friendly way to profile and
understand the E2E system behavior and deployment requirements.

Goals of the POSCA testsuite:
 a) Automatically locate the bottlenecks in a iterative manner.
 b) Automatically generate the testing report for bottlenecks in
different categories.
 c) Implementing Automated Staging.

Scopes of the POSCA testsuite:
 a) Modeling, Testing and Test Result analysis.
 b) Parameters choosing and Algorithms.

Test stories of POSCA testsuite:
 a) Factor test (Stress test): base test cases that Feature test and Optimization will be
dependant on.
 b) Feature test: test cases for features/scenarios.
 c) Optimization test: test to tune the system parameter.

Detailed workflow is illutrated below.
* TODO Add image here

Preinstall Packages
====================
* TODO Description of dependent packages

Run POSCA Locally
=================
* TO Description of POSCA testing steps

Run POSCA through Community CI
==============================
* TODO Description of POSCA integrated into CI system

Test Result Description
=======================
* TODO hwo to access the test result
