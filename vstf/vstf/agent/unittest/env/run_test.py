"""
Created on 2015-9-24

@author: y00228926
"""
import unittest
import importlib

test_order_list = [
    "vstf.agent.unittest.env.test_origin_driver",
    "vstf.agent.unittest.env.test_bridge_plugin",
    "vstf.agent.unittest.env.test_drivermanager",
    "vstf.agent.unittest.env.test_devicemanager",
    "vstf.agent.unittest.env.test_vs_plugin_manager",
    "vstf.agent.unittest.env.test_builder",
    "vstf.agent.unittest.env.test_sourcemanager",
]


def main():
    import logging
    logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    suite = unittest.TestSuite()
    for mod_name in test_order_list:
        mod = importlib.import_module(mod_name)
        suit = unittest.TestLoader().loadTestsFromModule(mod)
        suite.addTest(suit)
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    main()
