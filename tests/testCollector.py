# $Id$

import unittest
from AccessControl import Unauthorized

from CPSCollectorTestCase import CPSCollectorTestCase

def view_zpt(*args, **kwargs):

    pass

class TestCollector(CPSCollectorTestCase):
    def afterSetUp(self):
        CPSCollectorTestCase.afterSetUp(self)
        self.portal.collector_fake_view_zpt = view_zpt

        self.login('wsman')
        self.ws = self.portal.workspaces
        self.wftool = self.portal.portal_workflow

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

        self.submitted = getattr(self.portal.sections, oid)
        self.fakify(self.submitted)
        self.working = getattr(self.ws, oid)
        self.fakify(self.working)

    def beforeTearDown(self):
        del self.portal.collector_fake_view_zpt
        self.logout()

    # Collector objects hold the id of zpts to be called back
    def fakify(self, proxy):
        doc = proxy.getContent()
        doc._view_pt = 'collector_fake_view_zpt'
        doc._edit_pt = 'collector_view_zpt'

    def test_submitted_perms(self):
        REQUEST = self.app.REQUEST

        ## permissions on the submitted copy
        # No right to edit. We need a valid form, otherwise the editing
        # actions don't even get called.

        REQUEST.form = {'f_id' : 'name', 'type' : 'email',
                        'is_form_submitted' : 1}
        self.assertRaises(Unauthorized,self.submitted.Form_editField)
        self.assertRaises(Unauthorized,self.submitted.Form_delField,
                          REQUEST=REQUEST)

        self.assertRaises(Unauthorized,self.submitted.Form_moveFieldUp,
                          REQUEST=REQUEST)
        self.assertRaises(Unauthorized,self.submitted.Form_moveFieldDown,
                          REQUEST=REQUEST)
        self.assertRaises(Unauthorized,self.submitted.Data_erase,
                          REQUEST=REQUEST)

        # calling the fake view to check View perm and grab fields
        REQUEST.form = {}
        self.working.Form_view()



    ## permissions on the working copy
    def test_working_perms_add(self):
        REQUEST = self.app.REQUEST

        REQUEST.form = {'id' : 'newfield', 'type' : 'title'}
        self.working.Form_addField(REQUEST=REQUEST) # will also call Form_editField

    def test_working_perms_move_up(self):
        REQUEST = self.app.REQUEST

        REQUEST.form['f_id'] = 'number'
        self.working.Form_moveFieldUp(REQUEST=REQUEST)

    def test_working_perms_move_down(self):
        REQUEST = self.app.REQUEST

        REQUEST.form['f_id'] = 'name'
        self.working.Form_moveFieldDown(REQUEST=REQUEST)

    def test_working_perms_del(self):
        REQUEST = self.app.REQUEST

        REQUEST.form['f_id'] = 'number'
        self.working.Form_delField(REQUEST=REQUEST)

    def test_working_perms_data_erase(self):
        REQUEST = self.app.REQUEST

        self.working.Data_erase(REQUEST=REQUEST)

    def test_working_perms_export(self):
        REQUEST = self.app.REQUEST

        self.working.CollectorDocument_exportData(REQUEST=REQUEST)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCollector))
    return suite

if __name__ == '__main__':
    unittest.main()
