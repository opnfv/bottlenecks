##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import clize
from sigtools.modifiers import autokwoargs
from vstf.controller.settings.mail_settings import MailSettings
from vstf.controller.settings.perf_settings import PerfSettings
from vstf.controller.settings.cpu_settings import CpuSettings
from vstf.controller.settings.tool_settings import ToolSettings


@autokwoargs
def sinput(mail=False, perf=False, affctl=False, tool=False):
    """Settings command line input

    mail:  if start mail settings

    perf:  if start perf settings

    affctl:  if start set cpu affability

    tool:  if start set tool properties

    """

    if mail:
        MailSettings().sinput()
    if perf:
        PerfSettings().sinput()
    if affctl:
        CpuSettings().sinput()
    if tool:
        ToolSettings().sinput()


def main():
    clize.run(sinput)

if __name__ == '__main__':
    main()
