"""
Created on 2015-9-24

@author: y00228926
"""
import unittest
import importlib

test_order_list = [
    "vstf.agent.unittest.perf.test_utils",
    "vstf.agent.unittest.perf.test_netns",
    "vstf.agent.unittest.perf.test_netperf",
    "vstf.agent.unittest.perf.test_qperf",
    "vstf.agent.unittest.perf.test_pktgen",
    "vstf.agent.unittest.perf.test_vstfperf",
]


def main():
    import logging
    logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    suite = unittest.TestSuite()
    for mod_name in test_order_list:
        mod = importlib.import_module(mod_name)
        suit = unittest.TestLoader().loadTestsFromModule(mod)
        suite.addTest(suit)
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    main()
