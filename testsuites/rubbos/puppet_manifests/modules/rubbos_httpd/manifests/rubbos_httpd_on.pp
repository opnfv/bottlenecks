#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_httpd::rubbos_httpd_on {

  include params::rubbos_params
  require rubbos_common::rubbos_common_on

  # Declare some variables
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools

  # Prepare apache2 directory
  exec {'mkdir ${rubbos_app_tools}/apache2':
        command => "mkdir -p ${rubbos_app_tools}/apache2",
        creates => "${rubbos_app_tools}/apache2",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
  }

  # Prepare packages
  file {'${rubbos_app_tools}/httpd-2.0.64.tar.gz':
        ensure  => present,
        path    => "${rubbos_app_tools}/httpd-2.0.64.tar.gz",
        source  => "puppet:///modules/rubbos_httpd/httpd-2.0.64.tar.gz",
  }

  exec {'tar xzvf ${rubbos_app_tools}/httpd-2.0.64.tar.gz':
        cwd         => "${rubbos_app_tools}",
        command     => "tar xzvf ${rubbos_app_tools}/httpd-2.0.64.tar.gz",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => File['${rubbos_app_tools}/httpd-2.0.64.tar.gz'],
        refreshonly => true,
  }

  file {'${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz':
        ensure  => present,
        path    => "${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz",
        source  => "puppet:///modules/rubbos_httpd/tomcat-connectors-1.2.32-src.tar.gz",
  }

  exec {'tar xzvf ${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz':
        cwd         => "${rubbos_app_tools}",
        command     => "tar xzvf ${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => File['${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz'],
        refreshonly => true
  }

  # Add user and group
  group {'apache':
        name    => "apache",
        ensure  => present,
        before  => User['apache'],
  }
  user {'apache':
        name            => "apache",
        ensure          => present,
        groups          => "apache",
        password        => "apache",
        before          => Exec['${rubbos_app_tools}/httpd-2.0.64/configure'],
  }

  # Install apache http server
  exec {'${rubbos_app_tools}/httpd-2.0.64/configure':
        cwd         => "${rubbos_app_tools}/httpd-2.0.64",
        command     => "${rubbos_app_tools}/httpd-2.0.64/configure --prefix=${rubbos_app_tools}/apache2 --enable-module=so --enable-so --with-mpm=worker",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => Exec['tar xzvf ${rubbos_app_tools}/httpd-2.0.64.tar.gz'],
        refreshonly => true,
  }

  exec {'make httpd':
        cwd         => "${rubbos_app_tools}/httpd-2.0.64",
        command     => "make",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => Exec['${rubbos_app_tools}/httpd-2.0.64/configure'],
        refreshonly => true,
  }

  exec {'make install httpd':
        cwd         => "${rubbos_app_tools}/httpd-2.0.64",
        command     => "make install",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => Exec['make httpd'],
        refreshonly => true,
  }

  # Install mod jk
  exec {'${rubbos_app_tools}/tomcat-connectors-1.2.32-src/native/configure':
        cwd         => "${rubbos_app_tools}/tomcat-connectors-1.2.32-src/native",
        command     => "${rubbos_app_tools}/tomcat-connectors-1.2.32-src/native/configure --with-apxs=${rubbos_app_tools}/apache2/bin/apxs --enable-jni --with-java-home=${rubbos_app_tools}/jdk1.6.0_27",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => [
                    Exec['tar xzvf ${rubbos_app_tools}/tomcat-connectors-1.2.32-src.tar.gz'],
                    Exec['make install httpd']],
        refreshonly => true,
  }

  exec {'make mod jk':
        cwd         => "${rubbos_app_tools}/tomcat-connectors-1.2.32-src/native",
        command     => "make",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => Exec['${rubbos_app_tools}/tomcat-connectors-1.2.32-src/native/configure'],
        refreshonly => true,
  }

  exec {'make install mod jk':
        cwd         => "${rubbos_app_tools}/tomcat-connectors-1.2.32-src/native",
        command     => "make install",
        path        => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        subscribe   => Exec['make mod jk'],
        refreshonly => true,
  }

  # Config apache http server
  file {'${rubbos_app_tools}/apache2/conf/httpd.conf':
        ensure          => present,
        path            => "${rubbos_app_tools}/apache2/conf/httpd.conf",
        source          => "puppet:///modules/rubbos_httpd/apache_conf/httpd.conf",
        show_diff       => false,
        subscribe       => [Exec['make install httpd'],Exec['make install mod jk']],
  }

  file {'${rubbos_app_tools}/apache2/conf/workers.properties':
        ensure          => present,
        path            => "${rubbos_app_tools}/apache2/conf/workers.properties",
        source          => "puppet:///modules/rubbos_httpd/apache_conf/workers.properties",
        show_diff       => false,
        subscribe       => [Exec['make install httpd'],Exec['make install mod jk']],
  }

  file {'${rubbos_app_tools}/apache2/htdocs/rubbos':
        ensure          => present,
        path            => "${rubbos_app_tools}/apache2/htdocs/rubbos",
        recurse         => true,
        source          => "puppet:///modules/rubbos_httpd/apache_files/rubbos_html",
        show_diff       => false,
        subscribe       => [Exec['make install httpd'],Exec['make install mod jk']],
  }

  # Ensure apache2 service is running
  service {'apache http server':
        ensure          => running,
        hasstatus       => false,
        status          => "ps aux | grep 'bin/httpd.*start$'",
        start           => "${rubbos_app_tools}/apache2/bin/apachectl -f ${rubbos_app_tools}/apache2/conf/httpd.conf -k start",
        stop            => "${rubbos_app_tools}/apache2/bin/apachectl -f ${rubbos_app_tools}/apache2/conf/httpd.conf -k stop",
        subscribe       => [
                        File['${rubbos_app_tools}/apache2/conf/httpd.conf'],
                        File['${rubbos_app_tools}/apache2/conf/workers.properties']],
  }

}
