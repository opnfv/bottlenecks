#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_monitor::rubbos_monitor_off {

  include params::rubbos_params

  # Declare some variables
  $rubbos_app           = $params::rubbos_params::rubbos_app

  # Make uninstall sysstat
  exec {'make uninstall sysstat':
        cwd     => "${rubbos_app}/sysstat-9.0.6",
        command => "make uninstall",
	path    => ["/bin","/sbin","/usr/bin","/usr/sbin","/usr/local/bin","/usr/local/sbin"],
	onlyif	=> "test -d ${rubbos_app}/sysstat-9.0.6",
  }

  # Remove folder
  file {'${rubbos_app}/sysstat-9.0.6':
        ensure  => absent,
        path    => "${rubbos_app}/sysstat-9.0.6",
        force   => true,
	recurse	=> true,
        backup  => false,
        require	=> Exec['make uninstall sysstat'],
  }

}
