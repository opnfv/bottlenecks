#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_mysql::rubbos_mysql_on {

  include params::rubbos_params
  require rubbos_common::rubbos_common_on

  # Declare some variables
  $rubbos_app           = $params::rubbos_params::rubbos_app
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools
  $rubbos_home          = $params::rubbos_params::rubbos_home
  $mysql_user_group     = $params::rubbos_params::mysql_user_group
  $mysql_user_name      = $params::rubbos_params::mysql_user_name
  $mysql_user_password  = $params::rubbos_params::mysql_user_password

  # Add group and user
  group {'${mysql_user_group}':
        name    => "${mysql_user_group}",
        ensure  => present,
        before  => User['${mysql_user_name}'],
  }
  user {'${mysql_user_name}':
        name            => "${mysql_user_name}",
        ensure          => present,
        groups          => "${mysql_user_group}",
        password        => "${mysql_user_password}",
        before          => File['${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz'],
  }

  # Prepare needed packages for mysql installation
  package {'libaio-dev':
        ensure  => installed,
        before  => Exec['scripts/mysql_install_db --user=${mysql_user_name}'],
  }
  package {'libaio1':
        ensure  => installed,
        before  => Exec['scripts/mysql_install_db --user=${mysql_user_name}'],
  }

  # Prepare and install mysql
  file {'${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz':
        path    => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz",
        ensure  => present,
        source  => "puppet:///modules/rubbos_mysql/mysql-5.5.46-linux2.6-x86_64.tar.gz",
        backup  => false,
        notify  => Exec['tar -xf ${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz'],
  }

  exec {'tar -xf ${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz':
        cwd     => "${rubbos_app_tools}",
        command => "tar -xf ${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz",
        creates => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/scripts/mysql_install_db",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
  }

  exec {'ln -s ${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64 mysql':
        cwd             => "/usr/local",
        command         => "ln -s ${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64 mysql",
        path            => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe       => Exec['tar -xf ${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64.tar.gz'],
  }

  exec {'scripts/mysql_install_db --user=${mysql_user_name}':
        cwd     => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64",
        command => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/scripts/mysql_install_db --user=${mysql_user_name}",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => Exec['ln -s ${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64 mysql'],
  }

  # Prepare a script
  file {'${rubbos_home}/prepare_rubbos_mysql_db.sh':
        path            => "${rubbos_home}/prepare_rubbos_mysql_db.sh",
        ensure          => present,
        source          => "puppet:///modules/rubbos_mysql/prepare_rubbos_mysql_db.sh",
        backup          => false,
        show_diff       => false,
  }

  # Start mysql service
  service {'mysql':
        ensure          => running,
        hasstatus       => false,
        provider        => upstart,
        status          => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/support-files/mysql.server status | grep 'MySQL running'",
        start           => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/bin/mysqld_safe &",
        stop            => "${rubbos_app_tools}/mysql-5.5.46-linux2.6-x86_64/bin/mysqladmin shutdown",
        require         => Exec['scripts/mysql_install_db --user=${mysql_user_name}'],
  }

}
