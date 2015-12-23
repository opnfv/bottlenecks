import commands
import logging

LOG = logging.getLogger(__name__)


def execute(cmd=None, care_result=True):
    if not cmd:
        LOG.error('The cmd is None')
        return None
    try:
        (status, ret) = commands.getstatusoutput(cmd)
        if care_result and 0 != status:
            LOG.error('CMD<%(cmd)s> \nSTDOUT:\n%(ret)s.', {'cmd':cmd, 'ret':ret})
            return None
        else:
            return ret
    except Exception as e:
        raise e
