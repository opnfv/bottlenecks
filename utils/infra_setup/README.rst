==================
Infra Setup Guide
==================

This document gives the guide of how to set up the infrastructure for the use of bottlenecks test cases.

Create Instances for the Applications
=====================================

Firstly, there is a need to set up several instances for the applications which will be installed.

The script create_instances.sh will set up several instances, the parameters used in this script can be obtained according to the following,

Parameter $OPENRC_PATH is the path of where your admin-openrc.sh located, which includes the username and password of your openstack. Other parameters can be obtained under your openstack CLI as listed below,

+-------------+----------------------+
| parameter   | commond line commond |
+=============+======================+
| NET_ID      | neutron net-list     |
+-------------+----------------------+
| FLAVOR_TYPE | nova flavor-list     |
+-------------+----------------------+
| IMAGE_ID    | nova image-list      |
+-------------+----------------------+
| SEC_GROUP   | nova secgroup-list   |
+-------------+----------------------+

Add Floating IPs for the Instances
===================================

Check the available floating IPs::

 nova floating-ip-list

Check the status of the instances created::

 nova list

If there're no available floating IPs, to create one::

 nova floating-ip-create <ext_net_name>

replace <ext_net_name> with the external network in your environment.

Associate the floating IP address with the instance::

 nova add-floating-ip <instance name or ID> <allocated_floating_IP>


**Documentation tracking**

Revision: _sha1_

Build date:  _date_
