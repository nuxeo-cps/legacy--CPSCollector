# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# $Id$

"""
  Collector Document
"""

__version__ = '$Revision$'[11:-2]

### import
from random import randrange
import time
from re import match, sub

from OFS.Folder import Folder
from AccessControl import ClassSecurityInfo
from Globals import DTMLFile
from Globals import InitializeClass

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.NuxCPSDocuments.BaseDocument import BaseDocument, \
     BaseDocument_adder

from Form import Form
from CollectorItem import CollectorItem


factory_type_information = (
    {'id': 'Collector Document',
     'description': 'A Collector Document.',
     'title': '_portal_type_Collector Document',
     'content_icon': 'CollectorDocument_icon.gif',
     'product': 'GIL',
     'factory': 'addCollectorDocument',
     'meta_type': 'Collector Document',
     'immediate_view': 'CollectorDocument_editForm',
     'allow_discussion': 1,
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': '_action_view_',
                  'action': 'view',
                  'permissions': (View,)},
                 {'id': 'edit',
                  'name': '_action_modify_prop_',
                  'action': 'CollectorDocument_editForm',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'edit_form',
                  'name': '_action_modify_form_',
                  'action': 'Form_editForm',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'export',
                  'name': '_action_export_csv_',
                  'action': 'exportData',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'export',
                  'name': '_action_erase_data_',
                  'action': 'eraseData',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'create',
                  'name': '_action_create_',
                  'action': 'CollectorDocument_createForm',
                  'visible': 0,
                  'permissions': ()},
                 {'id': 'isdocument',
                  'name': 'isdocument',
                  'action': 'isdocument',
                  'visible': 0,
                  'permissions': ()},
                 {'id': 'issearchabledocument',
                  'name': 'issearchabledocument',
                  'action': 'issearchabledocument',
                  'visible': 0,
                  'permissions': ()},
                 ),
     
     },
    )


### class
class CollectorDocument(Form, BaseDocument):
    """
    Collector Document
    """

    meta_type = "Collector Document"

    security = ClassSecurityInfo()

    _properties = BaseDocument._properties + (
        {'id':'author', 'type':'string', 'mode':'w', 'label':'Author'},
        {'id':'submit_msg', 'type':'string', 'mode':'w', 'label':'Message'},
        {'id':'unique_submit', 'type':'boolean', 'mode':'w',
         'label':'Unique Submit'},
        )
    author=''

    def __init__(self, id, **kw):
        "Guess what it is." 
        BaseDocument.__init__(self, id, **kw)
        Form.__init__(self, id)
        self.unique_submit=1

    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        "Finilize the form init."
        self.post_init( msg_pt=self.CollectorDocument_msg )

    security.declareProtected(View, 'SearchableText')
    def SearchableText(self):
        "Used by the catalog for basic full text indexing."
        return '%s %s %s %s' % (self.title, self.description,
                                self.author, self.related_links)

    ### collector action
    security.declareProtected(View, 'action')
    def action(self, **kw):
        if self.unique_submit:
            id = self._check_unique()
            if id:
                self._delObject(id)
        id = self._create_id()
        self._setObject(id, CollectorItem(id, self.get_values()))
        msg = self.submit_msg
        return self._msg_pt(display_msg=msg, **kw)

    security.declareProtected(ModifyPortalContent, 'exportData')
    def exportData(self, **kw):
        "export"
        fields = self.getFList(1)
        s = self._list_to_csv(['_date', '_user', '_ip']+fields)
        for obj in self.objectValues('CollectorItem'):
            user, ip, d = self._decode_id(obj.id)
            d = time.strftime('%Y-%m-%dT%H:%M:%S', d)
            lv=[d, user, ip]
            for f in fields:
                lv.append(obj.data.get(f, ''))
            s += self._list_to_csv(lv)
        return s

    security.declareProtected(ModifyPortalContent, 'eraseData')
    def eraseData(self, **kw):
        "erase all item obj"
        for obj in self.objectValues():
            self._delObject(obj.id)
        return "ERASE DONE"

    security.declareProtected(ModifyPortalContent, 'initTest')
    def initTest(self):
        "test that init a form"
        self.add_field('title', type='title', label='Test form')
        self.add_field('name', type='string', label='Enter your name',
                        size=12, maxlength=12, required=1)
        self.add_field('Age', type='int', label='How old are you')
        self.add_field('Email', type='email',
                        label='Enter your email', size=17)
        self.add_field('isMale', type='checkbox',
                        label='Are you a Male', checked=1)
        self.add_field('rad_1', type='radio',
                        mvalue='radvalue_1|Label v1\n'+ 
                        'radvalue_2|Label v2\nradvalue_3|label v3',
                        checked='radvalue_2')
        self.add_field('rad_1', label='Radio choose')
        self.add_field('rad2', type='radio',
                        mvalue='value_1|Label 1\n'+ 
                        'value_2|Label v 2\nvalue_3|label 3')
        self.add_field('rad2', label='Radio 2 choose', checked='value_3')
        self.add_field('drop2', type='selection',
                        size='1', label='2 choose')
        self.add_field('drop2', mvalue='choix_1|choix n°1\n'+
                        'choix_2|Le choix 2\nchoix_3|Le 3eme choix')
        self.add_field('drop2', checked='choix_1')
        self.add_field('sep1', type='separator')
        self.add_field('submit', type='submit', label='GO',
                        value='view:method')
        return "DONE"


    ### Private 
    def _list_to_csv(self, t):
        l = ''
        for v in t:
            if v and (v.find('\n')!=-1 or v.find('"')!=-1 or \
                       v.find(',')!=-1):
                v = '"'+sub('"', '""', v)+'"'                
            l += str(v) + ','
        return l[:-1] + '\n'

    def _check_unique(self):
        # check if user/remote ip have already been collected
        mtools = self.portal_membership
        if mtools.isAnonymousUser():
            s = 'anonymous_'+self.REQUEST.environ.get('REMOTE_ADDR','')
        else:
            s = mtools.getAuthenticatedMember().getUserName()
        for id in self.objectIds('CollectorItem'):
            _u, _ip, d = self._decode_id(id)
            if id.find(s) != -1:
                return id
        return None

    def _create_id(self):
        # id format is like time_user_ip_random
        # 021126143959_member_127.0.0.1_814
        # todo: should add the wg/hierarchie one day
        id = time.strftime('%y%m%d%H%M%S', time.localtime())+'_'
        mtools = self.portal_membership
        if mtools.isAnonymousUser():
            id += 'anonymous_'
        else:
            id += mtools.getAuthenticatedMember().getUserName()+'_'
        id += self.REQUEST.environ.get('REMOTE_ADDR', 'unknown_ip')+'_'
        id += '%3.3d' % randrange(999)
        return id

    def _decode_id(self, id=''):
        # return a tuple (user,ip,date) or None for bad id
        m=match(r'^(\d+)_([^_]+)_([^_]+)_\d+$', id)
        if m is None:
            return None
        d=time.strptime(m.group(1), '%y%m%d%H%M%S')
        user=m.group(2)
        ip=m.group(3)
        return (user,ip, d)


InitializeClass(CollectorDocument)

def addCollectorDocument(dispatcher, id, REQUEST=None, **kw):
    """Add a Collector Document"""
    ob = CollectorDocument(id, **kw)
    return BaseDocument_adder(dispatcher, id, ob, REQUEST=REQUEST)

#EOF
