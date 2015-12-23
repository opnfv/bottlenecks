"""
Created on 2015-10-10

@author: y00228926
"""
import unittest

from vstf.common import ssh
from vstf.controller.unittest import model


class Test(model.Test):

    def setUp(self):
        super(Test, self).setUp()
        self.host = self.source_repo["ip"]
        self.user = self.source_repo["user"]
        self.passwd = self.source_repo["passwd"]


    def tearDown(self):
        super(Test, self).tearDown()


    def test_run_cmd(self):
        ssh.run_cmd(self.host, self.user, self.passwd, 'ls')


if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)
    unittest.main()