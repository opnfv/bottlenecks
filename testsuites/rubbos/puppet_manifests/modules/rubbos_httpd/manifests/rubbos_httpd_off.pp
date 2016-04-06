#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_httpd::rubbos_httpd_off {

  include params::rubbos_params

  # Declare some variables
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools

  # Ensure apache2 service is stopped
  service {'stop apache http server':
        ensure          => stopped,
        hasstatus       => false,
        status          => "ps aux | grep 'bin/httpd.*start$'",
        start           => "${rubbos_app_tools}/apache2/bin/apachectl -f ${rubbos_app_tools}/apache2/conf/httpd.conf -k start",
        stop            => "${rubbos_app_tools}/apache2/bin/apachectl -f ${rubbos_app_tools}/apache2/conf/httpd.conf -k stop",
  }

  # delete directory
  file {'${rubbos_app_tools}/httpd-2.0.64.tar.gz':
        ensure  => absent,
        path    => "${rubbos_app_tools}/httpd-2.0.64.tar.gz",
        force   => true,
        backup  => false,
  }

  file {'${rubbos_app_tools}/httpd-2.0.64':
        ensure  => absent,
        path    => "${rubbos_app_tools}/httpd-2.0.64",
        force   => true,
        recurse => true,
        backup  => false,
        require => Service['stop apache http server'],
  }

  file {'${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz':
        ensure  => absent,
        path    => "${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz",
        force   => true,
        backup  => false,
  }

  file {'${rubbos_app_tools}/tomcat-connectors-1.2.32-src':
        ensure  => absent,
        path    => "${rubbos_app_tools}/tomcat-connectors-1.2.32-src",
        force   => true,
        recurse => true,
        backup  => false,
        require => Service['stop apache http server'],
  }

  # Delete apache2 directory
  exec {'rm -rf ${rubbos_app_tools}/apache2':
        cwd             => "${rubbos_app_tools}/",
        command	        => "rm -rf ${rubbos_app_tools}/apache2",
        path            => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        onlyif		=> "test -d ${rubbos_app_tools}/apache2",
  }

  # delete user and group
  user {'apache':
        name            => "apache",
        ensure          => absent,
        groups          => "apache",
        password        => "apache",
        require         => [
                        File['${rubbos_app_tools}/httpd-2.0.64'],
                        File['${rubbos_app_tools}/tomcat-connectors-1.2.32-src'],
                        Exec['rm -rf ${rubbos_app_tools}/apache2']],
  }
  group {'apache':
        name    => "apache",
        ensure  => absent,
        require => User['apache'],
  }

}
