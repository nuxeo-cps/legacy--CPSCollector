# $Id$

import unittest
from Testing import ZopeTestCase
from AccessControl import Unauthorized

import CPSCollectorTestCase

def view_zpt(*args, **kwargs):

    pass

class TestCollector(CPSCollectorTestCase.CPSCollectorTestCase):
    def afterSetUp(self):
        self.portal.collector_fake_view_zpt = view_zpt

        self.CpsLogin('wsman')
        self.ws = self.portal.workspaces
        self.wftool = self.portal.portal_workflow
        dispatcher = self.ws.manage_addProduct['CPSCollector']
        dispatcher.addCollectorDocument('collector')
        self.collector = self.ws.collector

    def beforeTearDown(self):
        del self.portal.collector_fake_view_zpt
        self.logout()

    # Collector objects hold the id of zpts to be called back
    def fakify(self, proxy):
        doc = proxy.getContent()
        doc._view_pt = 'collector_fake_view_zpt'
        doc._edit_pt = 'collector_view_zpt'

    def test_security(self):
        # prepare a doc
        oid = self.ws.invokeFactory('Collector Document', 'tosubmit')
        ob = getattr(self.ws, oid)
        collector = ob.getContent()
        collector.add_field('name', type='string')
        collector.add_field('number', type='int')

        # submit
        self.wftool.doActionFor(ob, 'copy_submit',
                           dest_container='sections',
                           initial_transition='submit')

        submitted = getattr(self.portal.sections, oid)
        self.fakify(submitted)
        working = getattr(self.ws, oid)
        self.fakify(working)

        REQUEST = self.app.REQUEST

        ## permissions on the submitted copy
        # No right to edit. We need a valid form, otherwise the editing
        # actions don't even get called.

        REQUEST.form = {'f_id' : 'name', 'type' : 'email',
                        'is_form_submitted' : 1}
        self.assertRaises(Unauthorized, submitted.Form_editField)
        self.assertRaises(Unauthorized, submitted.Form_delField,
                          REQUEST=REQUEST)

        self.assertRaises(Unauthorized, submitted.Form_moveFieldUp,
                          REQUEST=REQUEST)
        self.assertRaises(Unauthorized, submitted.Form_moveFieldDown,
                          REQUEST=REQUEST)
        self.assertRaises(Unauthorized, submitted.Data_erase,
                          REQUEST=REQUEST)

        

        ## permissions on the working copy

        REQUEST.form = {'id' : 'title', 'type' : 'title'}
        working.Form_addField(REQUEST=REQUEST) # will also call Form_editField

        REQUEST.form['f_id'] = 'title' # normally has already been done
        working.Form_moveFieldUp(REQUEST=REQUEST)
        working.Form_moveFieldDown(REQUEST=REQUEST)
        working.Form_delField(REQUEST=REQUEST)

        # calling the fake view to check View perm and grab fields
        REQUEST.form = {}
        working.Form_view() 
        
        working.Data_erase(REQUEST=REQUEST)

        REQUEST.form = {}
        fields = submitted.Form_view()
        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCollector))
    return suite

if __name__ == '__main__':
    unittest.main()
