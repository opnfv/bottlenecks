'''
Created on 2015-7-23

@author: y00228926
'''
import os
import logging
from stat import S_ISDIR
import Queue
import shutil
import paramiko
from paramiko.ssh_exception import AuthenticationException

LOG = logging.getLogger(__name__)


class SSHClientContext(paramiko.SSHClient):
    def __init__(self, ip, user, passwd, port=22):
        self.host = ip
        self.user = user
        self.passwd = passwd
        self.port = port
        super(SSHClientContext, self).__init__()

    def sync_exec_command(self, cmd):
        _, stdout, stderr = self.exec_command(cmd)
        ret = stdout.channel.recv_exit_status()
        out = stdout.read().strip()
        err = stderr.read().strip()
        LOG.info("in %s,%s,return:%s,output:%s:error:%s" % (self.host, cmd, ret, out, err))
        return ret, out, err

    def connect(self):
        super(SSHClientContext, self).connect(self.host, self.port, self.user, self.passwd, timeout=10)

    def __enter__(self):
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type == AuthenticationException:
            return False


class SFTPClientContext(object):
    def __init__(self, ip, user, passwd, port=22):
        self.host = ip
        self.passwd = passwd
        self.user = user
        self.port = port

    def connect(self):
        self.t = paramiko.Transport((self.host, self.port))
        self.t.connect(username=self.user, password=self.passwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

    def get(self, remote, local):
        self.sftp.get(remote, local)

    def put(self, local, remote):
        self.sftp.put(local, remote)

    def mkdir(self, path):
        self.sftp.mkdir(path)

    def rmdir(self, path):
        self.sftp.rmdir(path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == TypeError:
            return False
        return False


def upload_conf_file(host, user, passwd, src, dst):
    with SFTPClientContext(host, user, passwd) as ftp:
        ftp.connect()
        LOG.info('putting file:%s to %s:%s' % (src, host, dst))
        ftp.put(src, dst)


def upload_dir(host, user, passwd, local_dir, remote_dir):
    assert remote_dir.startswith('/')
    assert local_dir != '/'
    while local_dir.endswith('/'):
        local_dir = local_dir[:-1]
    while remote_dir.endswith('/'):
        remote_dir = remote_dir[:-1]
    remote_dir = os.path.join(remote_dir, os.path.basename(local_dir))
    ret, _, _ = run_cmd(host, user, passwd, "sudo rm -rf %s" % remote_dir)
    if ret != 0 and ret != 1:
        LOG.error("somehow failed in rm -rf %s on host:%s,return:%s" % (remote_dir, host, ret))
        exit(1)
    with SFTPClientContext(host, user, passwd) as sftp:
        sftp.connect()
        for root, dirs, files in os.walk(local_dir):
            for filename in files:
                local_file = os.path.join(root, filename)
                remote_file = local_file.replace(local_dir, remote_dir)
                try:
                    sftp.put(local_file, remote_file)
                except IOError:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file, remote_file)
                LOG.info("upload %s to remote %s" % (local_file, remote_file))
            for name in dirs:
                local_path = os.path.join(root, name)
                remote_path = local_path.replace(local_dir, remote_dir)
                try:
                    sftp.mkdir(remote_path)
                    LOG.info("mkdir path %s" % remote_path)
                except Exception, e:
                    raise
    return remote_dir


def isdir(path, sftp):
    exists = True
    is_dir = False
    file_stat = None
    try:
        file_stat = sftp.stat(path).st_mode
        is_dir = S_ISDIR(file_stat)
    except IOError:
        exists = False
    return exists, is_dir, file_stat


def download_file(host, user, passwd, remote_path, local_path):
    assert not remote_path.endswith('/')
    remote_file_name = os.path.basename(remote_path)
    if local_path.endswith('/'):
        if not os.path.exists(local_path):
            raise Exception('path:%s not exist.' % local_path)
        dest = os.path.join(local_path, remote_file_name)
    else:
        if os.path.isdir(local_path):
            dest = os.path.join(local_path, remote_file_name)
        else:
            dir_path = os.path.dirname(local_path)
            if not os.path.exists(dir_path):
                raise Exception('path:%s not exist' % dir_path)
            dest = local_path
    transport = paramiko.Transport((host, 22))
    transport.connect(username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    exists, is_dir, st = isdir(remote_path, sftp)
    if exists and not is_dir:
        sftp.get(remote_path, dest)
        os.chmod(dest, st)
    else:
        raise Exception('error:cannot find the file or file is dir')
    return True


def download_dir(host, user, passwd, remote_path, local_path):
    while remote_path.endswith('/'):
        remote_path = remote_path[:-1]
    if local_path.endswith('/'):
        if not os.path.exists(local_path):
            raise Exception('path:%s not exist.' % local_path)
        dest_path = os.path.join(local_path, os.path.basename(remote_path))
    else:
        if os.path.isdir(local_path):
            dest_path = os.path.join(local_path, os.path.basename(remote_path))
        else:
            dir_name = os.path.dirname(local_path)
            if os.path.exists(dir_name):
                dest_path = local_path
            else:
                raise Exception('path:%s is not exists' % dir_name)
    LOG.info("download_dir from host:%s:%s to dest:%s" % (host, remote_path, dest_path))
    transport = paramiko.Transport((host, 22))
    transport.connect(username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    exists, is_dir, _ = isdir(remote_path, sftp)
    if exists and is_dir:
        q = Queue.Queue(0)
        q.put(remote_path)
        while not q.empty():
            path = q.get()
            st = sftp.lstat(path).st_mode
            relative_path = path[len(remote_path):]
            if relative_path.startswith('/'): relative_path = relative_path[1:]
            local = os.path.join(dest_path, relative_path)
            if os.path.exists(local):
                shutil.rmtree(local)
            os.mkdir(local)
            os.chmod(local, st)
            file_list = sftp.listdir(path)
            for item in file_list:
                fullpath = os.path.join(path, item)
                _, is_dir, st = isdir(fullpath, sftp)
                if is_dir:
                    q.put(fullpath)
                else:
                    dest = os.path.join(local, item)
                    sftp.get(fullpath, dest)
                    os.chmod(dest, st)
    else:
        raise Exception('path:%s:%s not exists or is not a dir' % (host, remote_path))
    return dest_path


def run_cmd(host, user, passwd, cmd):
    with SSHClientContext(host, user, passwd) as ssh:
        ssh.connect()
        ret, stdout, stderr = ssh.sync_exec_command(cmd)
    return ret, stdout, stderr


class SshFileTransfer(object):
    def __init__(self, ip, user, passwd):
        self.ip, self.user, self.passwd = ip, user, passwd

    def upload_dir(self, src, dst):
        return upload_dir(self.ip, self.user, self.passwd, src, dst)

    def download_dir(self, src, dst):
        download_dir(self.ip, self.user, self.passwd, src, dst)

    def upload_file(self, src, dst):
        upload_conf_file(self.ip, self.user, self.passwd, src, dst)

    def download_file(self, src, dst):
        download_file(self.ip, self.user, self.passwd, src, dst)
