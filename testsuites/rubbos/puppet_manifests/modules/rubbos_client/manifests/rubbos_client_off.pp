#############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class rubbos_client::rubbos_client_off {

  include params::rubbos_params

  # Declare some variables
  $rubbos_home          = $params::rubbos_params::rubbos_home

  # build.properties
  file {'${rubbos_home}/build.properties':
        ensure          => absent,
        path            => "${rubbos_home}/build.properties",
        show_diff       => false,
        backup          => false,
  }

  # config.mk
  file {'${rubbos_home}/config.mk':
        ensure          => absent,
        path            => "${rubbos_home}/config.mk",
        show_diff       => false,
        backup          => false,
  }

  # Makefile
  file {'${rubbos_home}/Makefile':
        ensure          => absent,
        path            => "${rubbos_home}/Makefile",
        show_diff       => false,
        backup          => false,
  }

  # Client/rubbos.properties.template
  file {'${rubbos_home}/Client/rubbos.properties.template':
        ensure          => absent,
        path            => "${rubbos_home}/Client/rubbos.properties.template",
        show_diff       => false,
        backup          => false,
  }

  # bench/run_emulator.sh
  file {'${rubbos_home}/bench/run_emulator.sh':
        ensure          => absent,
        path            => "${rubbos_home}/bench/run_emulator.sh",
        show_diff       => false,
        backup          => false,
  }

  file {'${rubbos_home}/Client.tar.gz':
      ensure            => absent,
      path              => "${rubbos_home}/Client.tar.gz",
      backup            => false,
  }

  file {'${rubbos_home}/Client':
        ensure          => absent,
        path            => "${rubbos_home}/Client",
        force           => true,
        recurse         => true,
        show_diff       => false,
        backup          => false,
  }

  file {'${rubbos_home}/workload.tar.gz':
        ensure          => absent,
        path            => "${rubbos_home}/workload.tar.gz",
        backup          => false,
  }

  file {'${rubbos_home}/workload':
        ensure          => absent,
        path            => "${rubbos_home}/workload",
        force           => true,
        recurse         => true,
        show_diff       => false,
        backup          => false,
  }

  file {'${rubbos_home}/database.tar.gz':
        ensure          => absent,
        path            => "${rubbos_home}/database.tar.gz",
        backup          => false,
  }

  file {'${rubbos_home}/database':
        ensure          => absent,
        path            => "${rubbos_home}/database",
        force           => true,
        recurse         => true,
        show_diff       => false,
        backup          => false,
  }

}
