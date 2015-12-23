from vstf.common import cliutil as util


@util.arg("--test",
          dest="test",
          default="",
          help="a params of test-xx")
@util.arg("--xx",
          dest="xx",
          default="",
          help="a params of test-xx")
def do_test_xx(args):
    """this is a help doc"""
    print "run test01 " + args.test + args.xx