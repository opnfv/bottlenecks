#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_monitor::rubbos_monitor_on {

  include params::rubbos_params
  require rubbos_common::rubbos_common_on

  # Declare some variables
  $rubbos_app           = $params::rubbos_params::rubbos_app
  $rubbos_home          = $params::rubbos_params::rubbos_home

  # Prepare bench folder and related files
  file {'${rubbos_home}/bench.tar.gz':
	ensure	=> file,
	path	=> "${rubbos_home}/bench.tar.gz",
	source	=> "puppet:///modules/rubbos_monitor/bench.tar.gz",
	backup	=> false,
  }

  exec {'tar zxvf ${rubbos_home}/bench.tar.gz':
	cwd		=> "${rubbos_home}",
        command 	=> "tar zxvf ${rubbos_home}/bench.tar.gz",
	path            => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
	subscribe	=> File['${rubbos_home}/bench.tar.gz'],
  }

  # Prepare monitoring tool
  file {'${rubbos_app}/sysstat-9.0.6.tar.gz':
        ensure  => file,
        path    => "${rubbos_app}/sysstat-9.0.6.tar.gz",
        source  => "puppet:///modules/rubbos_monitor/sysstat-9.0.6.tar.gz",
	backup	=> false,
  }

  exec {'tar xzvf ${rubbos_app}/sysstat-9.0.6.tar.gz':
        cwd     => "${rubbos_app}",
        command => "tar xzvf ${rubbos_app}/sysstat-9.0.6.tar.gz",
	path	=> ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => File['${rubbos_app}/sysstat-9.0.6.tar.gz'],
  }

  file {'flush_cache':
	ensure	=> file,
	path	=> "${rubbos_home}/bench/flush_cache",
	source	=> "puppet:///modules/rubbos_monitor/flush_cache",
	backup	=> false,
	mode	=> 0755,
	require	=> Exec['tar zxvf ${rubbos_home}/bench.tar.gz'],
  }

  file {'cpu_mem.sh':
	ensure	=> file,
	path	=> "${rubbos_app}/cpu_mem.sh",
	source	=> "puppet:///modules/rubbos_monitor/cpu_mem.sh",
	backup	=> false,
	mode	=> 0755,
  }

  # Build and install sysstat
  exec {'configure sysstat':
	cwd     => "${rubbos_app}/sysstat-9.0.6",
        command => "${rubbos_app}/sysstat-9.0.6/configure --prefix=${rubbos_app}/sysstat-9.0.6 --disable-nls",
	path	=> ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
	require	=> [
		Exec['tar xzvf ${rubbos_app}/sysstat-9.0.6.tar.gz'],
		Package['make'],Package['gcc'],Package['g++']],
  }

  exec {'make sysstat':
	cwd     => "${rubbos_app}/sysstat-9.0.6",
	command	=> "make",
	path	=> ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
	require	=> Exec['configure sysstat'],
  }

  exec {'make install sysstat':
	cwd     => "${rubbos_app}/sysstat-9.0.6",
        command => "make install",
	path	=> ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
        require => Exec['make sysstat'],
  }

}
