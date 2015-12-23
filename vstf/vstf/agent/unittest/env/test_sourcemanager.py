"""
Created on 2015-10-9

@author: y00228926
"""
import unittest
import shutil
import time
import os

from vstf.agent.env.basic.source_manager import SourceCodeManager
from vstf.agent.unittest.env import model


class TestSourceManager(model.Test):
    def setUp(self):
        super(TestSourceManager, self).setUp()
        self.sm = SourceCodeManager()
        self.dest_path = '/tmp/test_source_manager'
        os.mkdir(self.dest_path)

    def tearDown(self):
        shutil.rmtree(self.dest_path, ignore_errors = True)

    def _time(self,func):
        def _deco(*args):
            start_time = time.time()
            func(*args)
            end_time = time.time()
            return end_time - start_time
        return _deco

    def test_download_source_code(self):
        for key, item in self.source_repo.items():
            print self.source_repo
            url = item['url']
            target = os.path.join(self.dest_path, key)
            install = item['install']
            if install:
                self.sm._git_pull(url, target)
                self.assertTrue(os.path.isdir(target))
                my_download = self._time(self.sm._git_pull)
                t = my_download(url, target)
                self.assertTrue(t < 1.0)
            else:
                self.assertFalse(os.path.isdir(target))


if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)
    LOG = logging.getLogger(__name__)
    unittest.main()