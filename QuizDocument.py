# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# $Id$
"""
A Quiz is a special collector that only allows a few widgets
and checks user answers against correct answers provided by
the quiz creator
"""

from AccessControl import ClassSecurityInfo

from Globals import InitializeClass

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCollector.CollectorDocument import CollectorDocument, Form

from Products.CPSCore.CPSBase import CPSBase_adder

def BaseDocument_adder(disp, id, ob, REQUEST=None):
    return CPSBase_adder(disp, ob, REQUEST)

from zLOG import LOG, DEBUG

factory_type_information = (
    {'id': 'Quiz Document',
     'description': 'portal_type_QuizDocument_description',
     'title': 'portal_type_QuizDocument_title',
     'content_icon': 'CollectorDocument_icon.gif',
     'product': 'CPSCollector',
     'factory': 'addQuizDocument',
     'meta_type': 'Quiz Document',
     'immediate_view': 'CollectorDocument_editProp',
     'allow_discussion': 1,
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': 'action_view',
                  'action': 'Form_view',
                  'permissions': (View,)},
                 {'id': 'check_results',
                  'name': 'action_view_results',
                  'action': 'QuizDocument_viewResults',
                  'permissions': (View,)},
                 {'id': 'metadata',
                  'name': 'action_metadata',
                  'action': 'metadata_edit_form',
                  'permissions': (ModifyPortalContent,)
                  },
                 {'id': 'edit',
                  'name': 'action_modify_prop',
                  'action': 'CollectorDocument_editProp',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'edit_form',
                  'name': 'action_modify_form',
                  'action': 'Form_editQuizForm',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'export',
                  'name': 'action_export_csv',
                  'action': 'exportData',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'erase',
                  'name': 'action_erase_data',
                  'action': 'eraseData',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'create',
                  'name': 'action_create',
                  'action': 'CollectorDocument_createForm',
                  'visible': 0,
                  'permissions': ()},
                 ),
     'cps_proxy_type': 'document',
     'cps_is_searchable': 1,
     },
    )


class QuizDocument(CollectorDocument):
    """Quiz Document"""

    meta_type = "Quiz Document"

    security = ClassSecurityInfo()

    _properties = CollectorDocument._properties

    #overrides Form_editForm in Form.py
    _editForm_pt='Form_editQuizForm'
    
    def __init__(self, id, **kw):
        """Constructor"""
        CollectorDocument.__init__(self, id, **kw)
        self.add_field('trueval__', type='string', label='_form_good_answer_')
        QuizDocument.field_attr['checkbox'] = CollectorDocument.field_attr['checkbox'][:1] +\
                                              ('trueval__',) +\
                                              CollectorDocument.field_attr['checkbox'][1:]
        QuizDocument.field_attr['radio'] = CollectorDocument.field_attr['radio'][:2] +\
                                           ('trueval__',) +\
                                           CollectorDocument.field_attr['radio'][2:]
        QuizDocument.field_attr['vradio'] = CollectorDocument.field_attr['vradio'][:2] +\
                                            ('trueval__',) +\
                                            CollectorDocument.field_attr['vradio'][2:]
        
    security.declareProtected(View, 'get_quiz_fields')
    def get_quiz_fields(self, **kw):
        # Return the list of fields that can be used as quiz questions
        l = []
        for f in self.getFList(1):
            if self.fields[f]['type'] not in ('vradio','radio','checkbox'):
                continue
            l.append(f)
        return l

    security.declareProtected(View, 'check_answers')
    def check_quiz_answers(self, **kw):
        #retrieve latest filled form for current user
        latest_item = self._load_data()
        if latest_item:
            dt = latest_item.data
            fields = []
            nb_correct = 0
            for f_id in self.get_quiz_fields():
                #for each field, compare provided and correct answers
                #and build a field list with the following information
                #for each field: question, answer, correct answer, do
                #they match
                pa = self.process_answer(f_id,dt.get(f_id,None))
                if pa['is_correct']:
                    nb_correct = nb_correct + 1
                fields.append(pa)
            return {'fields': fields, 'nb_correct': nb_correct, 'nb_all': len(fields)}
        else:
            return {'fields': [], 'nb_correct': None, 'nb_all': None}
    

    def process_answer(self,f_id,f_value):
        #for a given field, compare answer with correct answer
        #build a summary of the question and result
        #question, answer, correct answer, do they match
        field = self.fields[f_id]
        result = {'question': field['label']}
        correct_answer = field['trueval']
        if field['type'] == 'checkbox':
            if ((correct_answer and not f_value) or
                (f_value and not correct_answer)):
                #this series of somewhat complex tests abstracts
                #other the correct value for the checkbox
                #any value that does not eval to None is considered
                #as 'checked' (this is the same behaviour as in the std
                #collector document)
                result['is_correct'] = 0
                if correct_answer:
                    result['correct_answ'] = 'checked'
                    result['chosen_answ'] = 'unchecked'
                else:
                    result['correct_answ'] = 'unchecked'
                    result['chosen_answ'] = 'checked'
            else:
                result['is_correct'] = 1
                if correct_answer:
                    result['correct_answ'] = 'checked'
                    result['chosen_answ'] = 'checked'
                else:
                    result['correct_answ'] = 'unchecked'
                    result['chosen_answ'] = 'unchecked'
        else:
            #for radio buttons
            if correct_answer == f_value:
                result['is_correct'] = 1
            else:
                result['is_correct'] = 0
            if field.has_key('mvalue'):
                result['correct_answ'] = field['mvalue'].get(correct_answer,
                                                             correct_answer)
                result['chosen_answ'] = field['mvalue'].get(f_value,
                                                            f_value)
            else:
                result['correct_answ'] = correct_answer
                result['chosen_answ'] = f_value
        return result

InitializeClass(QuizDocument)

def addQuizDocument(dispatcher, id, REQUEST=None, **kw):
    """ Add a Collector Document """
    ob = QuizDocument(id, **kw)
    return BaseDocument_adder(dispatcher, id, ob, REQUEST=REQUEST)

#EOF
