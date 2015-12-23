import subprocess
import threading
import logging
from vstf.common import constants

LOG = logging.getLogger(__name__)


class CommandLine(object):
    def __init__(self):
        super(CommandLine, self).__init__()
        self.proc = None
        self.is_timeout = False

    def __kill_proc(self):
        self.is_timeout = True
        self.proc.kill()

    def execute(self, cmd, timeout=constants.TIMEOUT, shell=False):
        """this func call subprocess.Popen(),
        here setup a timer to deal with timeout.
        :param cmd: cmd list like ['ls', 'home']
        :param timeout: for timer count for timeout
        :return: (ret, output) the output (stdout+'\n'+stderr)
        """
        # reset the timeout flag
        self.is_timeout = False
        self.proc = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=shell)

        timer = threading.Timer(timeout, self.__kill_proc, [])
        timer.start()
        stdout, stderr = self.proc.communicate()
        timer.cancel()

        if self.proc.returncode or self.is_timeout:
            if self.is_timeout:
                LOG.error("run cmd<%(cmd)s> timeout", {"cmd": cmd})
            ret = False
            output = "".join([stderr, stdout])
        else:
            ret = True
            output = stdout
        return ret, output
