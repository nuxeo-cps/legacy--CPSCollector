# $Id$

import unittest
from Testing import ZopeTestCase

import CPSCollectorTestCase

class TestCollector(CPSCollectorTestCase.CPSCollectorTestCase):
    def afterSetUp(self):
        self.login('manager')
        self.ws = self.portal.workspaces
        dispatcher = self.ws.manage_addProduct['CPSCollector']
        dispatcher.addCollectorDocument('collector')
        self.collector = self.ws.collector

    def test(self):
        # Don't test anything
        pass


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCollector))
    return suite

if __name__ == '__main__':
    unittest.main()
