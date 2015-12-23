'''
Created on 2015-9-28

@author: y00228926
'''
import unittest
import os

from vstf.controller.unittest import model
from vstf.controller.env_build import env_build


class TestEnvBuilder(model.Test):
    def setUp(self):
        super(TestEnvBuilder, self).setUp()
        self.dir = os.path.dirname(__file__)
        
    @unittest.skip('for now')
    def test_build_tn(self):
        filepath = os.path.join(self.dir,'../../../etc/vstf/env/Tn.json')
        self.mgr = env_build.EnvBuildApi(self.conn, filepath)
        ret = self.mgr.build()
        self.assertTrue(ret, "build_tn failed,ret = %s" % ret)
        
    @unittest.skip('for now')
    def test_build_tn1v(self):
        filepath = os.path.join(self.dir,'../../../etc/vstf/env/Tnv.json')
        self.mgr = env_build.EnvBuildApi(self.conn, filepath)
        ret = self.mgr.build()
        self.assertTrue(ret, "build_tn1v failed,ret = %s" % ret)
        
    @unittest.skip('for now')
    def test_build_ti(self):
        filepath = os.path.join(self.dir,'../../../etc/vstf/env/Ti.json')
        self.mgr = env_build.EnvBuildApi(self.conn, filepath)
        ret = self.mgr.build()
        self.assertTrue(ret, "build_ti failed,ret = %s" % ret)
        
    @unittest.skip('for now')
    def test_build_tu(self):
        filepath = os.path.join(self.dir,'../../../etc/vstf/env/Tu.json')
        self.mgr = env_build.EnvBuildApi(self.conn, filepath)
        ret = self.mgr.build()
        self.assertTrue(ret, "build_tu failed,ret = %s" % ret)
    
    def test_build_tu_bridge(self):
        filepath = os.path.join(self.dir,'../../../etc/vstf/env/Tu_br.json')
        self.mgr = env_build.EnvBuildApi(self.conn, filepath)
        ret = self.mgr.build()
        self.assertTrue(ret, "build_tu failed,ret = %s" % ret)
           
if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)
    unittest.main()