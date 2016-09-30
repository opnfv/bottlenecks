##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import argparse
import sys


class VstfHelpFormatter(argparse.HelpFormatter):

    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(VstfHelpFormatter, self).start_section(heading)


class VstfParser(argparse.ArgumentParser):

    def __init__(self,
                 prog='vstf',
                 description="",
                 epilog='',
                 add_help=True,
                 formatter_class=VstfHelpFormatter):

        super(VstfParser, self).__init__(
            prog=prog,
            description=description,
            epilog=epilog,
            add_help=add_help,
            formatter_class=formatter_class)
        self.subcommands = {}

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip()
            arguments = getattr(callback, 'arguments', [])
            subparser = subparsers.add_parser(
                command,
                help=action_help,
                description=desc,
                add_help=False,
                formatter_class=VstfHelpFormatter)
            subparser.add_argument('-h', '--help',
                                   action='help',
                                   help=argparse.SUPPRESS)
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def set_subcommand_parser(self, target, metavar="<subcommand>"):
        subparsers = self.add_subparsers(metavar=metavar)
        self._find_actions(subparsers, target)
        return subparsers

    def set_parser_to_subcommand(self, subparser, target):
        self._find_actions(subparser, target)


if __name__ == "__main__":
    from vstf.common import test_func
    parser = VstfParser(prog="vstf", description="test parser")
    parser.set_subcommand_parser(test_func)
    args = parser.parse_args(sys.argv[1:])
    args.func(args)
