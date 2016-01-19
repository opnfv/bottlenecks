===================================
Bottlenecks VSTF Installation Guide
===================================


VSTF Introduction
====================
VSTF(Virtual Switch Test Framework) is a system-level testing framework in the
area of network virtualization, and it could help you estimate the system switch
ability and find out the network bottlenecks by main KPIs(bandwidth, latency,
resource usage and so on), VSTF owns a methodology to define the test scenario and
testcases, Now we could support Tu testcases in the Openstack environment, More
scenarios and cases will be added.


Pre-install Packages on the ubuntu 14.04 VM
===========================================
VSTF VM Preparation Steps
-------------------------
1. Create a ubuntu 14.04 VM
2. Install dependency inside VM
3. Install vstf python package inside VM

VM preparation
--------------
Install python2.7 version and git

::

  sudo apt-get install python2.7
  sudo apt-get install git

Download Bottlenecks package

::
  sudo cd /home/
  sudo git clone https://gerrit.opnfv.org/gerrit/bottlenecks

Install the dependency

::

  sudo apt-get install python-pip
  pip install --upgrade pip
  dpkg-reconfigure dash
  sudo apt-get install libjpeg-dev
  sudo apt-get install libpng-dev
  sudo apt-get install python-dev
  sudo apt-get install python-testrepository
  sudo apt-get install git
  sudo apt-get install python-pika
  sudo apt-get install python-oslo.config
  sudo pip install -r /home/bottlenecks/vstf/requirements.txt

Install vstf package

::

  sudo mkdir -p /var/log/vstf/
  sudo cp -r /home/bottlenecks/vstf/etc/vstf/ /etc/
  sudo mkdir -p /opt/vstf/
  sudo cd /home/bottlenecks;sudo rm -rf build/
  sudo python setup.py install

Image on the Cloud
------------------
There is a complete vstf image on the cloud ,you could download it and use it to
deploy and run cases ,but do not need Step 1,2,3
vstf image URL: http://artifacts.opnfv.org/bottlenecks/vstf-manager-new.img
+-----------+-------------------------------------------------------------+
|    Name   | vstf-image                                                  |
+-----------+-------------------------------------------------------------+
|    URL    | http://artifacts.opnfv.org/bottlenecks/vstf-manager-new.img |
+-----------+-------------------------------------------------------------+
|   Format  | QCOW2                                                       |
+-----------+-------------------------------------------------------------+
|    Size   | 5G                                                          |
+-----------+-------------------------------------------------------------+
|    U/P    | username/password: root/root                                |
+-------------------------------------------------------------------------+


How is VSTF Integrated into Installers
========================================
VM requirements
---------------

m1.large means 4U4G for the target image Size 5GB
For the network used by VMs,network need two plane ,one plane is control plane and the other plane is test plane.
+--------------+----------+------------+--------------------------------------------------------------+
|     Name     |  flavor  | IMAGE_NAME | NETWORK                                                      |
+--------------+----------+------------+--------------------------------------------------------------+
| vstf-manager | m1.large | vstf-image | control-plane=XX.XX.XX.XX                                    |
+--------------+----------+------------+--------------------------------------------------------------+
| vstf-tester  | m1.large | vstf-image | control-plane(eth0)=XX.XX.XX.XX test-plane(eth1)=XX.XX.XX.XX |
+--------------+----------+------------+--------------------------------------------------------------+
| vstf-target  | m1.large | vstf-image | control-plane(eth0)=XX.XX.XX.XX test-plane(eth1)=XX.XX.XX.XX |
+--------------+----------+------------+--------------------------------------------------------------+

community CI system
-------------------
OPNFV community Jenkins Project for VSTF
+---------------------------------------+
| Project Name                          |
+---------------------------------------+
| bottlenecks-daily-fuel-vstf-lf-master |
+---------------------------------------+
| Project Categoty                      |
+---------------------------------------+
| bottlenecks                           |
+---------------------------------------+

Main Entrance for the ci test:

::

  cd /home/bottlenecks/ci;
  bash -x vstf_run.sh

Test on local(Openstack Environment)
------------------------------------
download the image file

::

  curl --connect-timeout 10 -o /tmp/vstf-manager.img http://artifacts.opnfv.org/bottlenecks/vstf-manager-new.img -v

create the image file by the glance

::

  glance image-create --name $MANAGER_IMAGE_NAME \
        --disk-format qcow2 \
        --container-format bare \
        --file /tmp/vstf-manager.img

create the keypair for the image(anyone will be ok)

::

  cd /home/bottlenecks/utils/infra_setup/bottlenecks_key
  nova keypair-add --pub_key $KEY_PATH/bottlenecks_key.pub $KEY_NAME

create the vstf three VMs in the openstack by heat

::

  cd /home/bottlenecks/utils/infra_setup/heat_template/vstf_heat_template
  heat stack-create vstf -f bottleneck_vstf.yaml

launch the vstf process inside the vstf-manager vstf-tester vstf-target VMs

::
  cd /home/bottlenecks/utils/infra_setup/heat_template/vstf_heat_template
  bash -x launch_vstf.sh

edit the test scenario and test packet list in the vstf_test.sh, now support the Tu-1/2/3

::
  function fn_testing_scenario(){
  ...
      local test_length_list="64 128 256 512 1024"
      local test_scenario_list="Tu-1 Tu-3"
  ...}

launch the vstf script

::
  cd /home/bottlenecks/utils/infra_setup/heat_template/vstf_heat_template
  bash -x vstf_test.sh

Test Result Description
=======================
Result Format
-------------
For example after the test, The result will display as the following format

::

  { u'64': { u'AverageLatency': 0.063,
             u'Bandwidth': 0.239,
             u'CPU': 0.0,
             u'Duration': 20,
             u'MaximumLatency': 0.063,
             u'MinimumLatency': 0.063,
             u'MppspGhz': 0,
             u'OfferedLoad': 100.0,
             u'PercentLoss': 22.42,
             u'RxFrameCount': 4309750.0,
             u'RxMbps': 198.28,
             u'TxFrameCount': 5555436.0,
             u'TxMbps': 230.03}}

Option Description
------------------
+---------------------+---------------------------------------------------+
|     Option Name     |                 Description                       |
+---------------------+---------------------------------------------------+
|    AverageLatency   | The average latency data during the packet        |
|                     | transmission (Unit:microsecond)                   |
+---------------------+---------------------------------------------------+
|      Bandwidth      | Network bandwidth(Unit:Million packets per second)|
+---------------------+---------------------------------------------------+
|         CPU         | Total Resource Cpu usage(Unit: Ghz)               |
+---------------------+---------------------------------------------------+
|      Duration       | Test time(Unit: second)                           |
+---------------------+---------------------------------------------------+
|   MaximumLatency    | The maximum packet latency during the packet      |
|                     | transmission (Unit:microsecond)                   |
+---------------------+---------------------------------------------------+
|   MinimumLatency    | The maximum packet latency during the packet      |
|                     | transmission (Unit:microsecond)                   |
+---------------------+---------------------------------------------------+
|      MppspGhz       | Million Packets per second with per CPU           |
|                     | resource Ghz(Unit: Mpps/Ghz)                      |
+---------------------+---------------------------------------------------+
|    OfferedLoad      | The load of network offered                       |
+---------------------+---------------------------------------------------+
|    PercentLoss      | The percent of frame loss rate                    |
+---------------------+---------------------------------------------------+
|    RxFrameCount     | The total frame on Nic rx                         |
+---------------------+---------------------------------------------------+
|       RxMbps        | The received bandwidth per second                 |
+---------------------+---------------------------------------------------+
|    TxFrameCount     | The total frame on Nic rx                         |
+---------------------+---------------------------------------------------+
|       TxMbps        | The send bandwidth per second                     |
+---------------------+---------------------------------------------------+
