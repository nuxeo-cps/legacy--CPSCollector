# $Id$

import unittest
from AccessControl import Unauthorized

from CPSCollectorTestCase import CPSCollectorTestCase
from Products.CPSCollector.upgrade import _upgrade_form_data_unicode
from Products.CPSCollector.upgrade import upgrade_data_unicode

class TestCollectorUnicodeUpgrade(CPSCollectorTestCase):
    def afterSetUp(self):
        CPSCollectorTestCase.afterSetUp(self)

        self.login('wsman')
        self.ws = self.portal.workspaces
        self.wftool = self.portal.portal_workflow

        # prepare a doc
        oid = self.ws.invokeFactory('Collector Document', 'tosubmit')
        ob = getattr(self.ws, oid)
        collector = self.collector = ob.getContent()
        collector.add_field('name', type='string')
        collector.add_field('text', type='text')
        collector.add_field('n\xf3m', type='string')

    def beforeTearDown(self):
        self.logout()

    def test_upgrade1(self):
        # basic case
        coll = self.collector
        coll._add_item('item1', dict(name='C\xe9sar', text="&#8230;"))
        coll._add_item('item2', {'n\xf3m' : 'ok'})
        _upgrade_form_data_unicode(coll)
        self.assertTrue(u'n\xf3m' in coll.fields)
        self.assertFalse('n\xf3m' in coll.fields)
        self.assertTrue(u'n\xf3m' in coll.fields_list)

        self.assertEquals(coll['item2'].data, {u'n\xf3m' : 'ok'})
        self.assertEquals(coll['item1'].data, {u'name' : u'C\xe9sar',
                                               u'text' : u'\u2026'})
        self.assertEquals(coll.getFList(), [u'name', u'text', u'n\xf3m'])

        exported = coll.exportData()

    def test_upgrade_radio(self):
        coll = self.collector
        coll.add_field('radio', type='radio', mvalue='aSeconde|Seconde\nbPremi\xe8re|Premi\xe8re\ncTerminale|Terminale')

        self.assertEquals(coll.fields['radio']['mvalue'],
                          {'aSeconde': 'Seconde',
                           'bPremi\xe8re': 'Premi\xe8re',
                           'cTerminale': 'Terminale'})
        _upgrade_form_data_unicode(coll)
        self.assertEquals(coll.fields[u'radio']['mvalue'],
                          {u'aSeconde': u'Seconde',
                           u'bPremi\xe8re': u'Premi\xe8re',
                           u'cTerminale': u'Terminale'})
        rendered = coll.Form_view_pt()

    def test_upgrade_whole(self):
        upgrade_data_unicode(self.portal)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCollectorUnicodeUpgrade))
    return suite

if __name__ == '__main__':
    unittest.main()
