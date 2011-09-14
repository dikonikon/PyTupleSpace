'''
Created on 16 Jun 2011

@author: dickon
'''
from logging.config import dictConfig
import unittest
import logging
from tuplespace import TupleSpace

class TestTupleSpace(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTupleSpace, self).__init__(*args, **kwargs)
        self.log = logging.getLogger(TestTupleSpace.__name__)
        self.log.setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def testRegistration(self):
        self.log.info("creating TupleSpace")
        t = TupleSpace("uri", "id", notify_asynch=False)
        t.register((1,2,3), "123")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()  