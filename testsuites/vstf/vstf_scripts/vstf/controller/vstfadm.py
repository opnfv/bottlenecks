##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import sys
import logging
import json
from vstf.common.vstfcli import VstfParser
from vstf.common import cliutil, constants, unix, message
from vstf.common.log import setup_logging
import vstf.common.constants as cst
import pprint

CONN = None


def print_stdout(msg):
    # out = json.dumps(message.get_body(message.decode(msg)), indent=2)
    out = message.get_body(message.decode(msg))
    pprint.pprint(out, indent=2)


def call(msg):
    """msg must be a dict"""
    msg = message.add_context(msg, corr=message.gen_corrid())
    CONN.send(message.encode(msg))
    return message.decode(CONN.recv())


def make_msg(method, **kwargs):
    return {"method": method, "args": kwargs}


@cliutil.arg("--host", dest="host", default="", action="store",
             help="list nic devices of specified host")
def do_list_devs(args):
    """List the host's all netdev."""
    ret = call(make_msg("list_devs", host=args.host))
    print_stdout(ret)


@cliutil.arg("--host", dest="host", action="store", default=None,
             help="which host to run src_install.")
@cliutil.arg("--config_file", dest="config_file", action="store", default=None,
             help="the git repo config.")
def do_src_install(args):
    """work agent to pull source code and compile.
    use git as underlying mechanism, please make sure the host has access to git repo.
    """
    ret = call(
        make_msg(
            "src_install",
            host=args.host,
            config_file=args.config_file))
    print_stdout(ret)


@cliutil.arg(
    "--host",
    dest="host",
    action="store",
    default=None,
    help="which host to build, must exists in your config file, use default[None] value to build all hosts.")
@cliutil.arg(
    "--model",
    dest="model",
    action="store",
    choices=(
        'Tn',
        'Ti',
        'Tu',
        'Tnv'),
    help="which model to build, if specified, the according config file /etc/vstf/env/{model}.json must exist.")
@cliutil.arg(
    "--config_file",
    dest="config_file",
    action="store",
    default=None,
    help="if specified, the config file will replace the default config file from /etc/vstf/env.")
def do_apply_model(args):
    """Apply model to the host."""
    ret = call(
        make_msg(
            "apply_model",
            host=args.host,
            model=args.model,
            config_file=args.config_file))
    print_stdout(ret)


@cliutil.arg("--host", dest="host", action="store", default=None,
             help="to which host you wish to create images")
@cliutil.arg("--config_file", dest="config_file", action="store", default=None,
             help="configuration file for image creation.")
def do_create_images(args):
    """create images on host, images are configed by configuration file."""
    ret = call(
        make_msg(
            "create_images",
            host=args.host,
            config_file=args.config_file))
    print_stdout(ret)


@cliutil.arg("--host", dest="host", action="store", default=None,
             help="to which host you wish to clean images")
@cliutil.arg("--config_file", dest="config_file", action="store", default=None,
             help="configuration file for images.")
def do_clean_images(args):
    """clean images on host, images are configed by configuration file."""
    ret = call(
        make_msg(
            "clean_images",
            host=args.host,
            config_file=args.config_file))
    print_stdout(ret)


@cliutil.arg(
    "--host",
    dest="host",
    action="store",
    default=None,
    help="which host to clean, must exists in your config file, use default[None] value to clean all hosts.")
@cliutil.arg(
    "--model",
    dest="model",
    action="store",
    choices=(
        'Tn',
        'Ti',
        'Tu',
        'Tnv'),
    help="if specified, the according config file /etc/vstf/env/{model}.json must exist.")
@cliutil.arg(
    "--config_file",
    dest="config_file",
    action="store",
    default=None,
    help="if specified, the config file will replace the default config file from /etc/vstf/env.")
def do_disapply_model(args):
    """Apply model to the host."""
    ret = call(
        make_msg(
            "disapply_model",
            host=args.host,
            model=args.model,
            config_file=args.config_file))
    print_stdout(ret)


@cliutil.arg("--host", dest="host", action="store",
             help="collect host information about cpu/mem etc")
def do_collect_host_info(args):
    """Show the host's CPU/MEN info"""
    ret = call(make_msg("collect_host_info", target=args.host))
    print_stdout(ret)


def do_show_tasks(args):
    """List history performance test tasks. Can be used by report cmd to generate reports.
    """
    ret = call(make_msg("list_tasks"))
    print_stdout(ret)


@cliutil.arg(
    "case",
    action="store",
    help="test case like Ti-1, Tn-1, Tnv-1, Tu-1, see case definition in documents")
@cliutil.arg("tool", action="store", choices=cst.TOOLS)
@cliutil.arg("protocol", action="store", choices=cst.TPROTOCOLS)
@cliutil.arg("type", action="store", choices=cst.TTYPES)
@cliutil.arg(
    "sizes",
    action="store",
    default="64",
    help='test size list "64 128"')
@cliutil.arg(
    "--affctl",
    action="store_true",
    help="when affctl is True, it will do affctl before testing")
def do_perf_test(args):
    """Runs a quick single software performance test without envbuild and generating reports.
    Outputs the result to the stdout immediately."""
    case_info = {
        'case': args.case,
        'tool': args.tool,
        'protocol': args.protocol,
        'type': args.type,
        'sizes': map(lambda x: int(x), args.sizes.strip().split())
    }
    ret = call(make_msg("run_perf_cmd",
                        case=case_info,
                        rpath=cst.REPORT_DEFAULTS,
                        affctl=args.affctl,
                        build_on=False,
                        save_on=False,
                        report_on=False,
                        mail_on=False
                        ))
    print_stdout(ret)


@cliutil.arg("-rpath",
             help="path of result",
             default=cst.REPORT_DEFAULTS,
             action="store")
@cliutil.arg("--report_off",
             help="when report_off is True, it will not generate the report",
             action="store_true")
@cliutil.arg("--mail_off",
             help="when mail_off is True, it will not send mail",
             action="store_true")
@cliutil.arg("--affctl",
             help="when affctl is True, it will do affctl before testing",
             action="store_true")
def do_batch_perf_test(args):
    """run soft performance test cases defined in /etc/vstf/perf/sw_perf.batch-settings"""
    ret = call(make_msg("run_perf_file",
                        affctl=args.affctl,
                        rpath=args.rpath,
                        report_on=not args.report_off,
                        mail_on=not args.mail_off
                        ))
    print_stdout(ret)


@cliutil.arg('-rpath',
             action='store',
             default=cst.REPORT_DEFAULTS,
             help=" the path name of test results  ")
@cliutil.arg("--mail_off",
             help="when mail_off is True, it will not send mail",
             action="store_true")
@cliutil.arg("--taskid",
             help="report depend of a history task id",
             default=-1,
             action="store")
def do_report(args):
    """generate the report from the database"""
    ret = call(make_msg("report",
                        rpath=args.rpath,
                        mail_off=args.mail_off,
                        taskid=args.taskid
                        ))
    print_stdout(ret)


@cliutil.arg("--conner",
             dest="conner",
             action="store",
             help="tester")
@cliutil.arg("--measurand",
             dest="measurand",
             action="store",
             help="tested")
@cliutil.arg("-m", "--model",
             dest="model",
             action="store",
             help="Test scene name : Tnv")
@cliutil.arg("-e", "--virtenv",
             dest="virtenv",
             action="store",
             help="virt env_build number(s): [1-8]")
@cliutil.arg("-q", "--queues",
             dest="queues",
             action="store",
             help="VM nic queues.")
@cliutil.arg("-f", "--flows",
             dest="flows",
             action="store",
             help="Flow queue(s) : [1-8]")
@cliutil.arg("-v", "--vlans",
             dest="vlans",
             action="store_true",
             help="vlan setting : 100-150;200-250")
@cliutil.arg("-d", "--direct",
             dest="direct",
             action="store",
             choices=["single", "double"],
             help="Flow Direction")
@cliutil.arg("-b", "--bind",
             dest="strategy",
             action="store",
             help="CPU bind strategy :  1 | 2 | 3 ")
@cliutil.arg("--config_file",
             dest="config_file",
             default='/etc/vstf/spirent/optimize.ini',
             action="store",
             help="config file for optimize.")
@cliutil.arg("--strategyfile",
             dest="strategyfile",
             default='/etc/vstf/spirent/strategy.ini',
             action="store",
             help="config file for strategy.")
def do_spirent_test(args):
    ret = call(make_msg("perf_test",
                        plugin="spirent",
                        conner=args.conner,
                        measurand=args.measurand,
                        virtenv=args.virtenv,
                        queues=args.queues,
                        direct=args.direct,
                        flows=args.flows,
                        strategy=args.strategy,
                        model=args.model,
                        vlans=args.vlans,
                        configfile=args.config_file,
                        strategyfile=args.strategyfile))
    print_stdout(ret)


@cliutil.arg("--host", dest="host", action="store", default=None,
             help="which host to list affctl info")
def do_affctl_list(args):
    ret = call(make_msg("affctl_list", host=args.host))
    print_stdout(ret)


@cliutil.arg("head", action="store", help="ip of head")
@cliutil.arg("tail", action="store", help="ip of tail")
def do_settings(args):
    ret = call(make_msg("settings", head=args.head, tail=args.tail))
    print_stdout(ret)


def main():
    parser = VstfParser(prog="vstfadm", description="vstf administration")
    parser.set_subcommand_parser(sys.modules[__name__], "functions")
    args = parser.parse_args()
    if args.func is None:
        sys.exit(-1)
    setup_logging(
        level=logging.DEBUG,
        log_file="/var/log/vstf/vstf-adm.log",
        clevel=logging.INFO)
    # connect to manage
    global CONN
    try:
        CONN = unix.UdpClient()
        CONN.connect(constants.sockaddr)
    except Exception as e:
        raise e

    args.func(args)
    # call functions of manage
    sys.exit(CONN.close())
