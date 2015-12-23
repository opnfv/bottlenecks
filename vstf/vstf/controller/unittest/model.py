"""
Created on 2015-9-28

@author: y00228926
"""
import unittest

from vstf.rpc_frame_work import rpc_producer
from vstf.controller.unittest import configuration


class Test(unittest.TestCase):

    def setUp(self):
        self.controller = configuration.rabbit_mq_server
        self.tester_host = configuration.tester_host
        self.target_host = configuration.target_host
        self.source_repo = configuration.source_repo
        self.conn = rpc_producer.Server(self.controller)

    def tearDown(self):
        self.conn.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()