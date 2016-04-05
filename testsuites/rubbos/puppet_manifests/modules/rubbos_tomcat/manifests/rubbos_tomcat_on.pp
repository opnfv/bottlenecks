#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_tomcat::rubbos_tomcat_on {

  include params::rubbos_params
  require rubbos_common::rubbos_common_on

  # Declare some variables
  $rubbos_app_tools     = $params::rubbos_params::rubbos_app_tools
  $rubbos_home          = $params::rubbos_params::rubbos_home

  # Prepare packages
  file {'${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz':
        ensure  => file,
        path    => "${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz",
        source  => "puppet:///modules/rubbos_tomcat/apache-tomcat-5.5.17.tar.gz",
        backup  => false,
  }

  exec {'tar xzvf ${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz':
        cwd     => "${rubbos_app_tools}",
        command => "tar xzvf ${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => File['${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz'],
  }

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

  # Override a config file: servier.xml
  file {'${rubbos_app_tools}/apache-tomcat-5.5.17/conf/server.xml':
        ensure          => file,
        path            => "${rubbos_app_tools}/apache-tomcat-5.5.17/conf/server.xml",
        source          => "puppet:///modules/rubbos_tomcat/server.xml",
        show_diff       => false,
        backup	        => false,
        require	        => Exec['tar xzvf ${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz'],
  }

  # Config tomcal_sl
  file {'${rubbos_home}/build.properties':
        ensure  => file,
        path    => "${rubbos_home}/build.properties",
        source  => "puppet:///modules/rubbos_tomcat/tomcat_sl/build.properties",
        backup  => false,
  }

  # Makefile
  file {'${rubbos_home}/Makefile':
        ensure  => file,
        path    => "${rubbos_home}/Makefile",
        source  => "puppet:///modules/rubbos_tomcat/tomcat_sl/rubbos_files/Makefile",
        backup  => false,
  }

  # config.mk
  file {'${rubbos_home}/config.mk':
        ensure  => file,
        path    => "${rubbos_home}/config.mk",
        source  => "puppet:///modules/rubbos_tomcat/tomcat_sl/rubbos_files/config.mk",
        backup  => false,
  }

  # servlets codes
  file {'${rubbos_home}/Servlets':
        ensure          => directory,
        path            => "${rubbos_home}/Servlets",
        recurse         => true,
        source          => "puppet:///modules/rubbos_tomcat/tomcat_sl/rubbos_files/Servlets",
        show_diff       => false,
        backup          => false,
  }

  # mysql.properties etc.
  file {'${rubbos_home}/Servlets/mysql.properties':
        ensure  => file,
        path    => "${rubbos_home}/Servlets/mysql.properties",
        source  => "puppet:///modules/rubbos_tomcat/tomcat_sl/mysql.properties",
        backup  => false,
  }

  file {'${rubbos_home}/Servlets/build.xml':
        ensure          => file,
        path            => "${rubbos_home}/Servlets/build.xml",
        source          => "puppet:///modules/rubbos_tomcat/tomcat_sl/build.xml",
        backup          => false,
        show_diff       => false,
        require         => File['${rubbos_home}/Servlets'],
  }

  file {'${rubbos_home}/Servlets/edu/rice/rubbos/servlets/Config.java':
        ensure  => file,
        path    => "${rubbos_home}/Servlets/edu/rice/rubbos/servlets/Config.java",
        source  => "puppet:///modules/rubbos_tomcat/tomcat_sl/Config.java",
        backup  => false,
        require => File['${rubbos_home}/Servlets'],
  }

  # mkdir for web.xml
  exec {'mkdir -p ${rubbos_home}/Servlet_HTML/WEB-INF':
        command => "mkdir -p ${rubbos_home}/Servlet_HTML/WEB-INF",
        creates => "${rubbos_home}/Servlet_HTML/WEB-INF",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
  }
  file {'${rubbos_home}/Servlet_HTML/WEB-INF/web.xml':
        ensure	=> file,
        path    => "${rubbos_home}/Servlet_HTML/WEB-INF/web.xml",
        source  => "puppet:///modules/rubbos_tomcat/tomcat_sl/web.xml",
        backup  => false,
        require => Exec['mkdir -p ${rubbos_home}/Servlet_HTML/WEB-INF'],
  }

  ## build rubbos.war
  exec {'ant clean':
        cwd             => "${rubbos_home}/Servlets",
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
                        File['${rubbos_home}/Servlets/mysql.properties'],
                        File['${rubbos_home}/Servlets/build.xml'],
                        File['${rubbos_home}/Servlets/edu/rice/rubbos/servlets/Config.java'],
                        File['${rubbos_home}/Servlet_HTML/WEB-INF/web.xml']],
  }

  exec {'ant dist':
        cwd             => "${rubbos_home}/Servlets",
        command         => "${rubbos_app_tools}/apache-ant-1.6.5/bin/ant dist",
        environment     => ["JAVA_HOME=${rubbos_app_tools}/jdk1.6.0_27","ANT_HOME=${rubbos_app_tools}/apache-ant-1.6.5"],
        path            => [                
                        "/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin",
                        "${rubbos_app_tools}/jdk1.6.0_27/bin",
                        "${rubbos_app_tools}/jdk1.6.0_27/jre/bin",
                        "${rubbos_app_tools}/apache-ant-1.6.5/bin"],
        subscribe       => Exec['ant clean'],
  } ## ant dist will generate: servlets.jar and rubbos.war
  
  exec {'deploy rubbos.war':
        cwd     => "${rubbos_app_tools}/apache-tomcat-5.5.17",
        command => "cp ${rubbos_home}/Servlets/rubbos.war ${rubbos_app_tools}/apache-tomcat-5.5.17/webapps/",
        onlyif  => "test -f ${rubbos_home}/Servlets/rubbos.war",
        path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => [
                Exec['ant dist'],
                Exec['tar xzvf ${rubbos_app_tools}/apache-tomcat-5.5.17.tar.gz']],
  }

  # Finally, start tomcat server
  exec {'${rubbos_app_tools}/apache-tomcat-5.5.17/bin/startup.sh':
        cwd             => "${rubbos_app_tools}/apache-tomcat-5.5.17",
        command	        => "${rubbos_app_tools}/apache-tomcat-5.5.17/bin/startup.sh",
        path            => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        environment     => "JAVA_HOME=${rubbos_app_tools}/jdk1.6.0_27",
        require	        => [
                        File['${rubbos_app_tools}/apache-tomcat-5.5.17/conf/server.xml'],
                        Exec['deploy rubbos.war']],
  }

}
