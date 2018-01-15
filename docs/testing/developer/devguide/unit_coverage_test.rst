.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd and others.

****************************************
Bottlenecks - Unit & Coverage Test Guide
****************************************


Introduction of the Rationale and Framework
===========================================

What are Unit & Coverage Tests
------------------------------

A unit test is an automated code-level test for a small and fairly isolated
part of functionality, mostly in terms of functions.
They should interact with external resources at their minimum, and includes
testing every corner cases and cases that do not work.

Unit tests should always be pretty simple, by intent. There are
a couple of ways to integrate unit tests into your development style `[1]`_:

* Test Driven Development, where unit tests are written prior to the functionality they're testing

* During refactoring, where existing code -- sometimes code without any automated tests to start with -- is retrofitted with unit tests as part of the refactoring process

# Bug fix testing, where bugs are first pinpointed by a targetted test and then fixed

* Straight test enhanced development, where tests are written organically as the code evolves.

Comprehensive and integrally designed unit tests serves valuably as
validator of your APIs, fuctionalities and the workflow that acctually
make them executable. It will make it possibe to deliver your codes
more quickly.

In the meanwhile, Coverage Test is the tool for measuring code coverage of Python programs. Accompany with Unit Test, it monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.

Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.

Why We Use a Framework and Nose
-------------------------------

People use unit test discovery and execution frameworks
so that they can forcus on add tests to existing code,
then the tests could be tirggerd,
resulting report could be obtained automatically.

In addition to adding and running your tests,
frameworks can run tests selectively according to your requirements, add coverage and profiling information, generate comprehensive reports.

There are many unit test frameworks in Python, and more arise every day.
It will take you some time to be falimiar with those
that are famous from among the ever-arising frameworks.
However, to us, it always matters more that you are actually
writing tests for your codes than how you write them.
Plus, nose is quite stable, it's been used by many projects and it could be adapted easily to mimic any other unit test discovery framework pretty easily.
So, why not?

Principles of the Tests
-----------------------

Before you actually implement test codes for your software,
please keep the following principles in mind `[2]`_

* A testing unit should focus on one tiny bit of functionality and prove it correct.

* Each test unit must be fully independent. This is usually handled by setUp() and tearDown() methods.

* Try hard to make tests that run fast.

* Learn your tools and learn how to run a single test or a test case. Then, when developing a function inside a module, run this function’s tests frequently, ideally automatically when you save the code.

* Always run the full test suite before a coding session, and run it again after. This will give you more confidence that you did not break anything in the rest of the code.

* It is a good idea to implement a hook that runs all tests before pushing code to a shared repository.

* If you are in the middle of a development session and have to interrupt your work, it is a good idea to write a broken unit test about what you want to develop next. When coming back to work, you will have a pointer to where you were and get back on track faster.

* The first step when you are debugging your code is to write a new test pinpointing the bug, while it is not always possible to do.

* Use long and descriptive names for testing functions. These function names are displayed when a test fails, and should be as descriptive as possible.

* Welly designed tests could acts as an introduction to new developers (read tests or write tests first before going into functionality development) and demonstrations for maintainers.


Offline Test
============

There only are a few guidance for developing and testing your code on your
local server assuming that you already have python installed.
For more detailed introduction,
please refer to the wesites of nose and coverage `[3]`_  `[4]`_.

Install Nose
------------

Install Nose using your OS's package manager. For example:

.. code-block:: bash

    pip install nose

As to creating tests and a quick start, please refer to `[5]`_

Run Tests
---------

Nose comes with a command line utility called 'nosetests'.
The simplest usage is to call nosetests from within your project directory
and pass a 'tests' directory as an argument. For example,

.. code-block:: bash
    
    nosetests tests

The outputs could be similar to the following summary:

.. code-block:: bash
    
     % nosetests tests
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s  OK

Adding Code Coverage
--------------------

Coverage is the metric that could complete your unit tests by overseeing
your test codes themselves.
Nose support coverage test according the Coverage.py.

.. code-block:: bash

    pip install coverage

To generate a coverage report using the nosetests utility,
simply add the --with-coverage. By default, coverage generates data
for all modules found in the current directory.

.. code-block:: bash

    nosetests --with-coverage

% nosetests --with-coverage --cover-package a

The --cover-package switch can be used multiple times to restrain the tests
only looking into the 3rd party package to avoid useless information. 

.. code-block:: bash

    nosetests --with-coverage --cover-package a --cover-package b
    ....
    Name    Stmts   Miss  Cover   Missing
    -------------------------------------
    a           8      0   100%
    ----------------------------------------------------------------------
    Ran 4 tests in 0.006sOK


OPNFV CI Verify Job
===================

Assuming that you have already got the main idea of unit testing
and start to programing you own tests under Bottlenecks repo.
The most important thing that should be clarified is that
unit tests under Bottlenecks should be either excutable offline and
by OPNFV CI pipeline.
When you submit patches to Bottlenecks repo, your patch should following certain ruls to enable the tests:

* The Bottlenecks unit tests are triggered by OPNFV verify job of CI
when you upload files to "test" directory.

* You should add your --cover-package and test directory in ./verify.sh
according to the above guides

After meeting the two rules, your patch will automatically validated by
nose tests executed by OPNFV verify job.


Reference
=========

_`[1]`: http://ivory.idyll.org/articles/nose-intro.html

_`[2]`: https://github.com/kennethreitz/python-guide/blob/master/docs/writing/tests.rst

_`[3]`: http://nose.readthedocs.io/en/latest/

_`[4]`: https://coverage.readthedocs.io/en/coverage-4.4.2

_`[5]`: http://blog.jameskyle.org/2010/10/nose-unit-testing-quick-start/
