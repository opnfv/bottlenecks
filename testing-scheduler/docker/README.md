# Brief Description
This is a description text file about the current directory: **docker**.

This directory contains the shell scripts which are used to build this project(**testing-scheduler**) as a dockerized application.

# Introduction & Manual
## 0. requirement

- a server host with linux os
- **docker** installed on the host 
- **docker-compose** installed on the host

## 1. docker containers
Built by these scripts, the dockerized application will contain 6 containers(1 + 1 + 4). They can be divided as three components:

* 1 server container: server component of **testing-scheduler**.
* 1 webUI container: ui component of **testing-scheduler**.
* a group of 4 containers of Conductor.

Correspondingly, there are three subdirectories in the current directory(**docker**):

* server: contains scirpts of running server container.
* ui: contains scirpts of running ui container.
* plugin:  contains scirpts of running Conductor containers.

The three subdirectories contains scripts respectively.The scripts (in one subdirectory) are used to build image and start container for single component.

## 2. commands
*NOTICE: run these commands under root account or use "sudo" before every command.*

### 2.1 general build
General build is used to build the 6 containers by only 2 steps.

In the current directory(**docker**), 

1. build all the docker images.

   > \# sh build.sh

   or use "sudo", like:
   > $ sudo sh build.sh

   (the commands below are similar).
2. start all the docker containers.

   > \# sh run.sh

the first command takes approximately 1h to finish(so need some patience :) ), and the latter one just takes a few minutes.

Essentially,  the **build.sh**  and **run.sh**(of the current directory(**docker**)) call the subdirectory scripts to build all three components.
### 2.2 build separetely
As said in 2.1, build step will need about 1h to finish.But it sometime will failed due to the network, and the rebuild will take a great time cost.So we can build and run the containers seperately according to the three subdirectories(**server**, **ui**, **plugin**).The steps are similar to the 2.1.

*IMPORTANT: There are relationships in these components(some need to be created before other).So you can only build the components below in the order: **plugin** -> **server** -> **ui***

* enter the subdirectory(**$dir** stands for **server**, **ui**, **plugin**).

  > \# cd $dir

* build the docker images.

  > \# sh build.sh

* run the docker containers.

  > \# sh run.sh
