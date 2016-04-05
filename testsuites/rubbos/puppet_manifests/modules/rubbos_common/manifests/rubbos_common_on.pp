##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_common::rubbos_common_on {
  
  include params::rubbos_params

  # Declare some variables
  $rubbos_app           = $params::rubbos_params::rubbos_app
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools
  $rubbos_home          = $params::rubbos_params::rubbos_home

  # Prepare RUBBOS_APP folder
  exec {'mkdir -p ${rubbos_app}':
        command => "mkdir -p ${rubbos_app}",
        unless  => "test -d ${rubbos_app}",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
  }

  # Prepare RUBBOS_APP_TOOLS folder 
  exec {'mkdir -p ${rubbos_app_tools}':
        command => "mkdir -p ${rubbos_app_tools}",
        unless  => "test -d ${rubbos_app_tools}",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
  }

  # Prepare RUBBOS_HOME folder
  exec {'mkdir -p ${rubbos_home}':
        command => "mkdir -p ${rubbos_home}",
        unless  => "test -d ${rubbos_home}",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => Exec['mkdir -p ${rubbos_app}'],
  }

  # Prepare common packages:
  package {'make':
        name    => "make",
        ensure  => installed,
  }
  package {'gcc':
        name    => "gcc",
        ensure  => installed,
  }
  package {'g++':
        name    => "g++",
        ensure  => installed,
  }

  # Install jdk
  file {'${rubbos_app_tools}/jdk-6u27-linux-x64.bin':
        ensure  => file,
        path    => "${rubbos_app_tools}/jdk-6u27-linux-x64.bin",
        source  => "puppet:///modules/rubbos_common/jdk-6u27-linux-x64.bin",
        mode    => 0711,
        backup  => false,
        require => Exec['mkdir -p ${rubbos_app_tools}'],
  }
  exec {'jdk-6u27-linux-x64.bin':
        cwd     => "${rubbos_app_tools}",
        command => "${rubbos_app_tools}/jdk-6u27-linux-x64.bin",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => File['${rubbos_app_tools}/jdk-6u27-linux-x64.bin'],
  }

}
