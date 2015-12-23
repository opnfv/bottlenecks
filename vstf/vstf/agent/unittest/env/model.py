"""
Created on 2015-10-9

@author: y00228926
"""
import unittest

from vstf.agent.unittest import configuration


class Test(unittest.TestCase):
    def setUp(self):
        self.eth_for_test = configuration.eth_for_test
        self.mac_of_eth = configuration.mac_of_eth
        self.source_repo = configuration.source_repo
        self.bdf_of_eth = configuration.bdf_of_eth

    def tearDown(self):
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
