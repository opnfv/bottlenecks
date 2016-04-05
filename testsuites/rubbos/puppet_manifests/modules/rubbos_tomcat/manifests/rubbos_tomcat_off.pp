#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_tomcat::rubbos_tomcat_off {

  include params::rubbos_params

  # Declare some variables
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools
  $rubbos_home          = $params::rubbos_params::rubbos_home

  # stop tomcat server
  exec {'${rubbos_app_tools}/apache-tomcat-5.5.17/bin/shutdown.sh':
        cwd             => "${rubbos_app_tools}/apache-tomcat-5.5.17",
        command         => "${rubbos_app_tools}/apache-tomcat-5.5.17/bin/shutdown.sh",
        path            => "/usr/bin:/usr/sbin:/bin:/sbin",
        environment     => "JAVA_HOME=${rubbos_app_tools}/jdk1.6.0_27",
        onlyif          => "test -f ${rubbos_app_tools}/apache-tomcat-5.5.17/bin/shutdown.sh",
        notify          => [
                        File['${rubbos_app_tools}/apache-tomcat-5.5.17'],
                        File['${rubbos_app_tools}/j2sdkee1.3.1'],
                        File['${rubbos_app_tools}/apache-ant-1.6.5'],	
	],
  }

  file {'${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz':
        ensure  => absent,
        path    => "${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz",
        backup  => false,
  }

  file {'${rubbos_app_tools}/apache-tomcat-5.5.17':
        ensure  => absent,
        path    => "${rubbos_app_tools}/apache-tomcat-5.5.17",
        force   => true,
        backup  => false,
  }

  file {'${rubbos_app_tools}/j2sdkee1.3.1.tar.gz':
        ensure  => absent,
        path    => "${rubbos_app_tools}/j2sdkee1.3.1.tar.gz",
        backup  => false,
  }

  file {'${rubbos_app_tools}/j2sdkee1.3.1':
        ensure  => absent,
        path    => "${rubbos_app_tools}/j2sdkee1.3.1",
	force	=> true,
        backup	=> false,
  }

  file {'${rubbos_app_tools}/apache-ant-1.6.5.tar.gz':
        ensure  => absent,
        path    => "${rubbos_app_tools}/apache-ant-1.6.5.tar.gz",
        backup  => false,
  }

  file {'${rubbos_app_tools}/apache-ant-1.6.5':
        ensure  => absent,
        path    => "${rubbos_app_tools}/apache-ant-1.6.5",
        force   => true,
        backup  => false,
  }

  file {'${rubbos_home}/Servlets':
        ensure  => absent,
        path    => "${rubbos_home}/Servlets",
        force   => true,
        recurse => true,
        backup  => false,
  }

}
