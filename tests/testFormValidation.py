"""
$Id$

you (may) need to make a symlink to run this testsuite:
ln -s $ZS/lib/python/Products $ZS/Products/CMFCore
"""
import unittest

import ZODB
import OFS.Application

from Products.GIL.Form import Form

def checkField(typ, val, **kw):
    ob = Form('utest')
    ob.add_field('foo', type=typ, **kw)
    ret = ob.check_field('foo', val)
    return ret

class TestFormValidation(unittest.TestCase):
    def setUp(self):
        # Set up some preconditions
        pass

    def tearDown(self):
        # Clean up after each test
        pass

    def test_required(self):
        ob = Form('utest')
        ob.add_field('string', type='string', required='on')
        ret = ob.check_field('string', '')
        self.assertEqual( ret, '_field_is_required_')

    def test_required(self):
        self.assertEqual(checkField('string', '', required='on'),
                         '_field_is_required_')
        self.assertEqual(checkField('string', None, required='on'),
                         '_field_is_required_')
        
    def test_string_maxlength_1(self):
        self.assertEqual(checkField('string', '1234', maxlength=4), None)
    def test_string_maxlength_2(self):
        self.assertEqual(checkField('string', '1234', maxlength=3),
                         '_field_is_too_long_')

    def test_float_1(self):
        self.assertEqual(checkField('float', '123,12'), None)
    def test_float_2(self):
        self.assertEqual(checkField('float', '1x3.12'), None)
    def test_float_3(self):
        self.assertEqual(checkField('float', '1a23'), None)

    def test_float_100(self):
        self.assertEqual(checkField('float', '12.12.23'),
                         '_field_float_invalid_')
    def test_float_101(self):
        self.assertEqual(checkField('float', '12a,23'),
                         '_field_float_invalid_')                         
    def test_float_102(self):
        self.assertEqual(checkField('float', 'x12'),
                         '_field_float_invalid_')                         


    def test_int_1(self):
        self.assertEqual(checkField('int', '1234567890'), None)
    def test_int_2(self):
        self.assertEqual(checkField('int', '001'), None)
    def test_int_3(self):
        self.assertEqual(checkField('int', '-0'), None)

    def test_int_100(self):
        self.assertEqual(checkField('int', '12.23'),
                         '_field_int_invalid_')
    def test_int_101(self):
        self.assertEqual(checkField('int', 'a1223'),
                         '_field_int_invalid_')                         
    def test_int_102(self):
        self.assertEqual(checkField('int', '12-12'),
                         '_field_int_invalid_')                         

    def test_identifier_1(self):
        self.assertEqual(checkField('identifier', 'id'), None)
    def test_identifier_2(self):
        self.assertEqual(checkField('identifier', 'b123_bla'), None)
    def test_identifier_3(self):
        self.assertEqual(checkField('identifier', 'A'), None)
    def test_identifier_4(self):
        self.assertEqual(checkField('identifier', 'Z1'), None)

    def test_identifier_100(self):
        self.assertEqual(checkField('identifier', '1bla'),
                         '_field_id_invalid_')
    def test_identifier_101(self):
        self.assertEqual(checkField('identifier', 'b-123'),
                         '_field_id_invalid_')        
    def test_identifier_102(self):
        self.assertEqual(checkField('identifier', '_bla'),
                         '_field_id_invalid_')        
    def test_identifier_102(self):
        self.assertEqual(checkField('identifier', 'a@bla'),
                         '_field_id_invalid_')        

    # testing with default 'en' locale
    def test_date_1(self):
        self.assertEqual(checkField('date', '01/01/2003'), None)
    def test_date_2(self):
        self.assertEqual(checkField('date', '12/31/2003'), None)
    def test_date_3(self):
        self.assertEqual(checkField('date', '1/1/2003'), None)
    def test_date_4(self):
        self.assertEqual(checkField('date', '01/01/1960'), None)
    def test_date_5(self):
        self.assertEqual(checkField('date', '01/01/1670'), None)
        
    def test_date_100(self):
        self.assertEqual(checkField('date', '13/12/2003'),
                         '_field_date_invalid_')
    def test_date_101(self):
        self.assertEqual(checkField('date', '12/32/2003'),
                         '_field_date_invalid_')        
    def test_date_102(self):
        self.assertEqual(checkField('date', '01/41/2003'),
                         '_field_date_invalid_')        
    def test_date_103(self):
        self.assertEqual(checkField('date', '01/01/03'),
                         '_field_date_invalid_')        


    def test_email_invalid_1(self):
        self.assertEqual(checkField('email', 'bla'),
                         '_field_email_invalid_')
    def test_email_invalid_2(self):
        self.assertEqual(checkField('email', 'bla@bla'),
                         '_field_email_invalid_')
    def test_email_invalid_3(self):
        self.assertEqual(checkField('email', 'bla.com'),
                         '_field_email_invalid_')
    def test_email_invalid_4(self):
        self.assertEqual(checkField('email', 'bla@bla.balzke'),
                         '_field_email_invalid_')
    def test_email_invalid_5(self):
        self.assertEqual(checkField('email', 'azer@bla.111'),
                         '_field_email_invalid_')
    def test_email_invalid_6(self):
        self.assertEqual(checkField('email', 'bla@bl az.com'),
                         '_field_email_invalid_')
    def test_email_invalid_7(self):
        self.assertEqual(checkField('email', 'bla@-.com'),
                         '_field_email_invalid_')
    def test_email_invalid_8(self):
        self.assertEqual(checkField('email', 'bla@qsdf.m'),
                         '_field_email_invalid_')
    def test_email_invalid_9(self):
        self.assertEqual(checkField('email', '@az.com'),
                         '_field_email_invalid_')
    def test_email_invalid_10(self):
        self.assertEqual(checkField('email', 'bla@qsdf@qsdlf.com'),
                         '_field_email_invalid_')
    def test_email_invalid_11(self):
        self.assertEqual(checkField('email', '@qsdf@qsldkfj.com'),
                         '_field_email_invalid_')
    def test_email_invalid_12(self):
        self.assertEqual(checkField('email', 'bla@.com'),
                         '_field_email_invalid_')

    def test_email_1(self):
        self.assertEqual(checkField('email', 'bla@bla.com'), None)
    def test_email_2(self):
        self.assertEqual(checkField('email', 'bla@bla.bla.com'), None)        
    def test_email_invalid_12(self):
        self.assertEqual(checkField('email', 'x@123.gouv'), None) 


    def test_selection_1(self):
        self.assertEqual(checkField('selection', 'sel3', multiple='on', 
                                    mvalue='sel1 | Section 1\nsel2 | Section 2\nsel3 | Section 3\nsel4 | Section 4\n'), None)
    def test_selection_2(self):
        self.assertEqual(checkField('selection', ['sel3','sel1'], multiple='on', 
                                    mvalue='sel1\nsel2\nsel3\n'), None)
    def test_selection_3(self):
        self.assertEqual(checkField('selection', 'sel3', multiple='on', 
                                    mvalue='sel1\nsel2\nsel3\n'), None)
    def test_selection_100(self):
        self.assertEqual(checkField('selection', 'sel4', multiple='on', 
                                    mvalue='sel1\nsel2\nsel3\n'),
                         '_field_selection_invalid_')
    def test_selection_101(self):
        self.assertEqual(checkField('selection', ['sel3','sel1'],
                                    multiple=None,
                                    mvalue='sel1\nsel2\nsel3\n'),
                         '_field_multiselect_invalid_')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFormValidation))
    return suite

if __name__ == '__main__':
    unittest.main()
