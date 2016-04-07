#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_client::rubbos_client_on {

  include params::rubbos_params
  require rubbos_common::rubbos_common_on
  require rubbos_monitor::rubbos_monitor_on

  # Declare some variables
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools
  $rubbos_home          = $params::rubbos_params::rubbos_home
  $rubbos_os_username   = $params::rubbos_params::rubbos_os_username
  $rubbos_os_usergroup  = $params::rubbos_params::rubbos_os_usergroup

  # Prepare needed tools
  file {'${rubbos_app_tools}/j2sdkee1.3.1.jar.gz':
        ensure  => file,
        path    => "${rubbos_app_tools}/j2sdkee1.3.1.jar.gz",
        source  => "puppet:///modules/rubbos_common/j2sdkee1.3.1.jar.gz",
        backup  => false,
  }

  exec {'tar xzvf ${rubbos_app_tools}/j2sdkee1.3.1.jar.gz':
        cwd     => "${rubbos_app_tools}",
        command => "tar xzvf ${rubbos_app_tools}/j2sdkee1.3.1.jar.gz",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => File['${rubbos_app_tools}/j2sdkee1.3.1.jar.gz'],
  }

  file {'${rubbos_app_tools}/apache-ant-1.6.5.tar.gz':
        ensure  => file,
        path    => "${rubbos_app_tools}/apache-ant-1.6.5.tar.gz",
        source  => "puppet:///modules/rubbos_common/apache-ant-1.6.5.tar.gz",
        backup  => false,
  }

  exec {'tar xzvf ${rubbos_app_tools}/apache-ant-1.6.5.tar.gz':
        cwd     => "${rubbos_app_tools}",
        command => "tar xzvf ${rubbos_app_tools}/apache-ant-1.6.5.tar.gz",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => File['${rubbos_app_tools}/apache-ant-1.6.5.tar.gz'],
  }

  # Prepare client codes and files
  file {'${rubbos_home}/Client.tar.gz':
       ensure   => file,
       path     => "${rubbos_home}/Client.tar.gz",
       source   => "puppet:///modules/rubbos_client/Client.tar.gz",
       backup   => false,
  }

  exec {'tar xvzf ${rubbos_home}/Client.tar.gz':
       cwd      => "${rubbos_home}",
       command  => "tar xvzf ${rubbos_home}/Client.tar.gz",
       path     => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
       require  => File['${rubbos_home}/Client.tar.gz'],
  }

  file {'${rubbos_home}/workload.tar.gz':
       ensure   => file,
       path     => "${rubbos_home}/workload.tar.gz",
       source   => "puppet:///modules/rubbos_client/workload.tar.gz",
       backup   => false,
  }

  exec {'tar xvzf ${rubbos_home}/workload.tar.gz':
       cwd      => "${rubbos_home}",
       command  => "tar xvzf ${rubbos_home}/workload.tar.gz",
       path     => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
       require  => File['${rubbos_home}/workload.tar.gz'],
  }

  file {'${rubbos_home}/database.tar.gz':
       ensure   => file,
       path     => "${rubbos_home}/database.tar.gz",
       source   => "puppet:///modules/rubbos_client/database.tar.gz",
       backup   => false,
  }

  exec {'tar xvzf ${rubbos_home}/database.tar.gz':
       cwd      => "${rubbos_home}",
       command  => "tar xvzf ${rubbos_home}/database.tar.gz",
       path     => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
       require  => File['${rubbos_home}/database.tar.gz'],
  }

  # build.properties
  file {'${rubbos_home}/build.properties':
        ensure          => file,
        path            => "${rubbos_home}/build.properties",
        source          => "puppet:///modules/rubbos_client/build.properties",
        show_diff       => false,
        backup          => false,
  }

  # config.mk
  file {'${rubbos_home}/config.mk':
        ensure          => file,
        path            => "${rubbos_home}/config.mk",
        source          => "puppet:///modules/rubbos_client/config.mk",
        show_diff       => false,
        backup          => false,
  }

  # Makefile
  file {'${rubbos_home}/Makefile':
        ensure          => file,
        path            => "${rubbos_home}/Makefile",
        source          => "puppet:///modules/rubbos_client/Makefile",
        show_diff       => false,
        backup          => false,
  }

  # rubbos.properties.template
  file {'${rubbos_home}/bench/rubbos.properties.template':
        ensure          => file,
        path            => "${rubbos_home}/bench/rubbos.properties.template",
        source          => "puppet:///modules/rubbos_client/rubbos.properties.template",
        show_diff       => false,
        backup          => false,
  }

  # executable scripts
  file {'${rubbos_home}/bench/run_emulator.sh':
        ensure          => file,
        path            => "${rubbos_home}/bench/run_emulator.sh",
        source          => "puppet:///modules/rubbos_client/run_emulator.sh",
        backup          => false,
  }

  # Build rubbos_client.jar
  exec {'ant clean':
        cwd             => "${rubbos_home}/Client",
        command         => "${rubbos_app_tools}/apache-ant-1.6.5/bin/ant clean",
        environment     => ["JAVA_HOME=${rubbos_app_tools}/jdk1.6.0_27","ANT_HOME=${rubbos_app_tools}/apache-ant-1.6.5"],
        path            => [
                        "/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin",
                        "${rubbos_app_tools}/jdk1.6.0_27/bin",
                        "${rubbos_app_tools}/jdk1.6.0_27/jre/bin",
                        "${rubbos_app_tools}/apache-ant-1.6.5/bin"],
        require         => [
                        Exec['tar xzvf ${rubbos_app_tools}/j2sdkee1.3.1.jar.gz'],
                        Exec['tar xzvf ${rubbos_app_tools}/apache-ant-1.6.5.tar.gz'],
                        File['${rubbos_home}/build.properties'],
                        File['${rubbos_home}/Makefile'],
                        File['${rubbos_home}/config.mk'],
                        Exec['tar xvzf ${rubbos_home}/Client.tar.gz']],
                        #File['${rubbos_home}/Client']],
  }

  exec {'ant jar':
        cwd             => "${rubbos_home}/Client",
        command         => "${rubbos_app_tools}/apache-ant-1.6.5/bin/ant jar",
        environment     => ["JAVA_HOME=${rubbos_app_tools}/jdk1.6.0_27","ANT_HOME=${rubbos_app_tools}/apache-ant-1.6.5"],
        path            => [
                        "/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin",
                        "${rubbos_app_tools}/jdk1.6.0_27/bin",
                        "${rubbos_app_tools}/jdk1.6.0_27/jre/bin",
                        "${rubbos_app_tools}/apache-ant-1.6.5/bin"],
        subscribe       => Exec['ant clean'],
  }

  # Change owner and group for the Client folder
  exec {'chown -R ${rubbos_os_username}:${rubbos_os_usergroup} ${rubbos_home}/Client':
        cwd             => "${rubbos_home}",
        command         => "chown -R ${rubbos_os_username}:${rubbos_os_usergroup} ${rubbos_home}/Client",
        path            => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require         => Exec['ant jar'],
  }

}
