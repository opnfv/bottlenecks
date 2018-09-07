.. This work is licensed under a Creative Commons Attribution 4.0 International License.
   .. http://creativecommons.org/licenses/by/4.0
      .. (c) Huawei Technologies Co.,Ltd and others.

***************************************************
Kubenetes Stress Test of Deployment Capacity
***************************************************

Test Case
=========

+-----------------------------------------------------------------------------+
|Bottlenecks Kubestone Deployment Capacity Test                               |
|                                                                             |
+--------------+--------------------------------------------------------------+
|test case name| kubestone_deployment_capacity                                |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|description   | Stress test regarding capacity of deployment                 |
+--------------+--------------------------------------------------------------+
|configuration | config file:                                                 |
|              |    testsuite/kubestone/testcases/deployment.yaml             |
|              |                                                              |
|              |                                                              |
+--------------+--------------------------------------------------------------+
|test result   | Capcity, Life-Cycle Duration, Available Deployments          |
|              |                                                              |
+--------------+--------------------------------------------------------------+

Configuration
============
::

  apiVersion: apps/v1
  kind: Deployment
  namespace: bottlenecks-kubestone
  test_type: Horizontal-Scaling
  scaling_steps: 10, 50, 100, 200
  template: None
  metadata:
    name: nginx-deployment
    labels:
      app: nginx
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: nginx
    template:
      metadata:
        labels:
          app: nginx
      spec:
        containers:
        - name: nginx
          image: nginx:1.7.9
          ports:
          - containerPort: 80

