#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_mysql::rubbos_mysql_off {

  include params::rubbos_params

  # Declare some variables
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools
  $mysql_user_group     = $params::rubbos_params::mysql_user_group
  $mysql_user_name      = $params::rubbos_params::mysql_user_name
  $mysql_user_password  = $params::rubbos_params::mysql_user_password

  file {'${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz':
        path    => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz",
        ensure  => absent,
        backup  => false,
  }

  # Stop mysql
  service {'stop mysql':
        ensure          => stopped,
        hasstatus       => false,
        provider        => "upstart",
        status          => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/support-files/mysql.server status | grep 'MySQL running'",
        start           => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/bin/mysqld_safe &",
        stop            => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/bin/mysqladmin shutdown",
  }

  file {'${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64':
        ensure  => absent,
        path    => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64",
        force   => true,
        recurse => true,
        backup  => false,
        require => Service['stop mysql'],
  }

  # Remove user and group
  user {'${mysql_user_name}':
        name            => "${mysql_user_name}",
        ensure          => absent,
        groups          => "${mysql_user_group}",
        password        => "${mysql_user_password}",
        require         => File['${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64'],
  }

  group {'${mysql_user_group}':
        name    => "${mysql_user_group}",
        ensure  => absent,
        require => User['${mysql_user_name}'],
  }

  # Remove softlink
  exec {'rm -rf /usr/local/mysql':
        cwd     => "/usr/local",
        command => "rm -rf /usr/local/mysql",
        onlyif  => "test -h /usr/local/mysql",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => Group['mysql'],
  }

  # Remove packages
  package {'libaio-dev':
        ensure  => absent,
  }
  package {'libaio1':
        ensure  => absent,
  }

}
