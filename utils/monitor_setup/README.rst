..
.. image:: ../etc/opnfv-logo.png
  :height: 40
  :width: 200
  :alt: OPNFV
  :align: left
..
|
|
Monitor Setup guide
===================

This document gives the guide of how to set up monitor tools used in Bottlenecks project.

Zabbix
=========

Zabbix is the ultimate enterprise-level software designed for real-time monitoring of millions of metrics collected from tens of thousands of servers, virtual machines and network devices. Zabbix is Open Source and comes at no cost.

The link https://www.zabbix.com/documentation/2.2/manual/installation/install_from_packages gives the instalation guide of Zabbix in linux servers. After the installation of Zabbix server and agent, there is a need to configure the .conf files

.. code-block:: bash

   vim /etc/zabbix/zabbix_agentd.conf

       Server=<Server_IP>
       ServerActive=<Server_IP>
       Hostname=<Agent_IP>

To add the Zabbix agent host to be monitored, please click Configuration->Hosts->Create host on the Zabbix server dashboard.

Revision: _sha1_

Build date: |today|
