# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# $Id$
"""
A Collector is a Form container, the form action store user input
into CollectorItem that can be exported as csv file.
Collector is able to display stat on data collected.
"""

import time
from random import randrange
from re import match, sub
from types import StringType, ListType

from OFS.Folder import Folder
from AccessControl import ClassSecurityInfo
from Globals import DTMLFile
from Globals import InitializeClass
from Acquisition import aq_base
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

try:
    # CPS3
    from Products.NuxCPS3.CPSBase import CPSBaseDocument as BaseDocument, \
         CPSBase_adder
    def BaseDocument_adder(disp, id, ob, REQUEST=None):
        return CPSBase_adder(disp, ob, REQUEST)
except ImportError:
    # CPS2
    from Products.NuxCPSDocuments.BaseDocument import BaseDocument, \
         BaseDocument_adder
    
from Products.NuxCPSCollector.Form import Form
from Products.NuxCPSCollector.CollectorItem import CollectorItem

factory_type_information = (
    {'id': 'Collector Document',
     'description': 'A Collector Document.',
     'title': '_portal_type_Collector Document',
     'content_icon': 'CollectorDocument_icon.gif',
     'product': 'NuxCPSCollector',
     'factory': 'addCollectorDocument',
     'meta_type': 'Collector Document',
     'immediate_view': 'CollectorDocument_editForm',
     'allow_discussion': 1,
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': '_action_view_',
                  'action': 'view',
                  'permissions': (View,)},
                 {'id': 'view_stat',
                  'name': '_action_view_stat_',
                  'action': 'viewStat',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'edit',
                  'name': '_action_modify_prop_',
                  'action': 'CollectorDocument_editForm',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'edit_form',
                  'name': '_action_modify_form_',
                  'action': 'editForm',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'export',
                  'name': '_action_export_csv_',
                  'action': 'exportData',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'erase',
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


class CollectorDocument(Form, BaseDocument):
    """ Collector Document """
    
    meta_type = "Collector Document"
    
    security = ClassSecurityInfo()
    
    _properties = BaseDocument._properties + (
        {'id':'submit_msg', 'type':'string', 'mode':'w',
         'label':'Message after submit'},
        {'id':'submit_msg_stat', 'type':'boolean', 'mode':'w',
         'label':'View statistic after submit'},
        {'id':'unique_submit', 'type':'boolean', 'mode':'w',
         'label':'Unique Submit'},
        {'id':'persistent_data', 'type':'boolean', 'mode':'w',
         'label':'Persistent data'},
        )
    submit_msg=''
    submit_msg_stat=0
    unique_submit=1
    persistent_data=0
    
    def __init__(self, id, **kw):
        """ Guess what it is """
        BaseDocument.__init__(self, id, **kw)
        Form.__init__(self, id)
        
    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        """ Finilize the form init """
        self.post_init(msg_pt='CollectorDocument_msg')
        BaseDocument.manage_afterAdd(self, item, container)

    security.declareProtected(View, 'SearchableText')
    def SearchableText(self):
        """ Used by the catalog for basic full text indexing """
        return '%s %s %s' % (self.title, self.description,
                                self.related_links)
    
    
    # WEB INTERFACE --------------------------------------------------
    security.declareProtected(View, 'view')
    def view(self, **kw):
        """ override view to handle persitent input """
        self._set_status()
        status,err=self.check_form()
        if status == 'valid_form':
            return self.action(**kw)
        
        if status == 'not_yet_submited' and self.persistent_data:
            obj = self._load_data()
            if obj:
                self.set_values(obj.data)
                status, err = self.check_form()
                
        if err:
            self._set_status(err)
              
        return self._display_zpt(self._view_pt, **kw)
    
    security.declareProtected(View, 'display')
    def display(self, **kw):
        """ displaying a non editable form with lastest input """
        input = self._load_data()
        if input:
                self.set_values(input.data)
                status, err = self.check_form()
        if err:
            self._set_status(err)
        _macros = self._macros_pt
        self._macros_pt = 'Form_displayMacros'
        ret = self._display_zpt(self._view_pt)
        self._macros_pt = _macros
        return ret
        
    security.declareProtected(View, 'action')
    def action(self, **kw):
        """ store valid input into a collector item """
        if self.unique_submit:
            id = self._check_unique()
            if id:
                self._delObject(id)
        id = self._create_id()
        self._setObject(id, CollectorItem(id, self.get_values()))
        return self._display_zpt(self._msg_pt, display_msg=self.submit_msg)

    
    security.declareProtected(ModifyPortalContent, 'exportData')
    def exportData(self, **kw):
        """ export all collected data as csv file """
        fields = self.getFList(1)
        s = self._list_to_csv(['_date', '_user', '_ip']+fields)
        for obj in self.objectValues('CollectorItem'):
            user, ip, d = self._decode_id(obj.id)
            if not user:
                continue
            d = time.strftime('%Y-%m-%dT%H:%M:%S', d)
            lv=[d, user, ip]
            for f in fields:
                lv.append(obj.data.get(f, ''))
            s += self._list_to_csv(lv)
        resp = self.REQUEST.RESPONSE
        filename=self.title_or_id()+'.csv'
        resp.setHeader('Content-Type', 'application/octet-stream')
        resp.setHeader('Content-Disposition', 'filename='+filename)        
        resp.setHeader('Cache-Control', 'no-cache')
        return s
    
    security.declareProtected(ModifyPortalContent, 'eraseData')
    def eraseData(self, **kw):
        """ erase all collector item """
        mcat = self.portal_messages
        psm='portal_status_message=%s' % (mcat('_form_erased_data_'), )
        for id in self.objectIds('CollectorItem'):
            self._delObject(id)
        self.REQUEST.RESPONSE.redirect('%s/?%s' % (self.absolute_url(), psm))
        return
    
    security.declareProtected(ModifyPortalContent, 'viewStat')
    def viewStat(self, **kw):
        "display stat for fields of type: selection/checkbox/radio"
        return self.CollectorDocument_viewStat(**kw)
    
    security.declareProtected(ModifyPortalContent, 'initTest')
    def initTest(self):
        """ test that init a form with all kind of field """
        self.add_field('title', label='This is a title', type='title')
        self.add_field('string', label='This is a string', type='string', required='on', maxlength='14', join='on', size='16')
        self.add_field('string_ro', label='This is a read only string:', value='Read only value', type='string_ro')
        self.add_field('id', label='This is an identifier', type='identifier', maxlength='14', join='on', size='16')
        self.add_field('email', label='this is an email', type='email')
        self.add_field('url', label='This is an URL', type='url', join='on')
        self.add_field('date', label='this is a date', type='date')
        self.add_field('pwd', label='This is a passwd', type='password', join='on')
        self.add_field('int', label='This is an integer', type='int')
        self.add_field('float', label='This is a float', type='float', join='on')
        self.add_field('phone', label='This is a phone number', type='phone')
        self.add_field('text', label='This is a text area', cols='60', type='text', rows='4')
        self.add_field('rad', label='This is a radio', checked='radio2', mvalue='radio1 | radio1\nradio2 | radio2\nradio3 | radio3\nradio4 | radio4\n', type='radio')
        self.add_field('cb', label='This is a checkbox', type='checkbox')
        self.add_field('selection', label='This is a selection', join='on', multiple='on', checked='sel3', mvalue='sel1 | Section 1\nsel2 | Section 2\nsel3 | Section 3\nsel4 | Section 4\n', type='selection')
        self.add_field('sel2', label='This is also a selection', checked='sel3', mvalue='sel1 | sel1\nsel2 | sel2\nsel3 | sel3\nsel4 | sel4\n', type='selection')
        self.add_field('newsel', label='bla selection', mvalue='poi1 | poi1\npoi4 | poi4\npoi7 | poi7\n', type='selection')
        self.add_field('sep', label='This is a separator', type='separator')
        self.add_field('bt', label='a SUBMIT button', join='on', type='submit')
        self.add_field('reset_bt', label='This is a reset button', type='reset')
        self.add_field('hidden', value='hidden value', type='hidden')
        self.add_field('comment', label='This is a comment !', type='comment')
        return "init Test DONE"
    
    security.declareProtected(ModifyPortalContent, 'initTestSurvey')
    def initTestSurvey(self):
        """ test that init a form with multilang survey """
        self.add_field('survey_title', label='_survey_title_', type='title')
        self.add_field('survey_id', label='_survey_bla_', value='12345', type='comment')
        self.add_field('survey_q1', label='_survey_q1_', checked='kind2', mvalue='kind1 | _survey_r1_\nkind2 | _survey_r2_\nkind3 | _survey_r3_\n', type='selection')
        self.add_field('survey_q2', label='_survey_q2_', multiple='on', checked='sel3', mvalue='sel1 | _survey_s1_\nsel2 | _survey_s2_\nsel3 | _survey_s3_\n', type='radio')
        self.add_field('survey_bt', label='_survey_bt_', type='submit')
        return "init Test Survey DONE"
    
    
    # ZPT INTERFACE --------------------------------------------------
    security.declareProtected(View, 'get_stat_fields')
    def get_stat_fields(self, **kw):
        # return the list of field with statistic
        l=[]
        for f in self.getFList(1):
            if self.fields[f]['type'] not in ('checkbox','radio','selection'):
                continue
            l.append(f)
        return l
    
    security.declareProtected(View, 'compute_stat')
    def compute_stat(self, **kw):
        # compute stat on selection/radio or checkbox fields
        r = {}
        date_start = time.localtime()
        date_end = time.localtime(0)
        nb_item=0
        
        for f in self.get_stat_fields():
            r[f]={}
            mv=self.fields[f].get('mvalue')
            if mv:
                for v in mv.keys():
                    r[f][v]=0
            else:
                r[f]['on']=0
                
        for obj in self.objectValues('CollectorItem'):
            _u, _ip, d = self._decode_id(obj.id)
            if not _u:
                continue
            if d < date_start:
                date_start = d
            if d > date_end:
                date_end = d
            nb_item += 1
            for f in r.keys():
                mv = obj.data.get(f)
                if not mv:
                    continue
                if type(mv) is StringType:
                    mv = [mv,]
                for v in mv:
                    if r[f].get(v,-1) != -1:
                        r[f][v] += 1
                        
        if nb_item:
            for f in r.keys():
                for v in r[f].keys():
                    nb = r[f][v]
                    r[f][v] = '%3.f' % (nb * 100.0 / nb_item)
        mcat = self.portal_messages
        date_start=time.strftime(mcat('_date_%m/%d/%Y %H:%M'), date_start)
        date_end=time.strftime(mcat('_date_%m/%d/%Y %H:%M'), date_end)
        r['_stat']={ 'nb_item':nb_item, 'date_start':date_start,
                     'date_end':date_end }
        return r
    
    
    # INTERNAL --------------------------------------------------
    security.declarePrivate('_load_data')
    def _load_data(self, item_id=None):
        """ load collectorItem data or latest if item_id is None """
        if not item_id:
            item_id = self._find_latest_item()
        if not item_id:
            return
        
        return getattr(aq_base(self), item_id)
    
    security.declarePrivate('_find_latest_item')
    def _find_latest_item(self):
        """ find the latest collectorItem id for the current logged user
        this feature does not work for anonymous user !
        """
        user, ip, d = self._decode_id(self._create_id())
        if user == 'anonymous':
            return
        
        match_id = None
        match_d = 0
        #log( 'Search '+ user+'_'+ip+':')

        for id in self.objectIds('CollectorItem'):
            user_, ip_, d_ = self._decode_id(id)
            if user == user_:
                if user == 'anonymous' and ip != ip_:
                    continue;
                #log( user+'_'+ip_ +': ok')
                if d_ > match_d:
                    match_id = id
                    match_d = d_
        return match_id
    
    security.declarePrivate('_list_to_csv')
    def _list_to_csv(self, t):
        """ convert list object into csv format """
        l = ''
        for v in t:
            if v and type(v) is ListType:
                _s = ''
                for vv in v:
                    _s += str(vv)+'+'
                if _s:
                    v = _s[:-1]
                else:
                    v = ''
            if v and (v.find('\n')!=-1 or v.find('"')!=-1 or \
                       v.find(',')!=-1):
                v = '"'+sub('"', '""', v)+'"'
            if not v:
                v=''
            l += str(v) + ', '
        if l:
            l=l[:-2]
        return l + '\n'
    
    security.declarePrivate('_check_unique')
    def _check_unique(self):
        """ check if user/remote ip have already been collected """
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

    security.declarePrivate('_create_id')
    def _create_id(self):
        """ id format is like time_user_ip_random
        021126143959_member_127.0.0.1_814 """
        id = time.strftime('%y%m%d%H%M%S', time.localtime())+'_'
        mtools = self.portal_membership
        if mtools.isAnonymousUser():
            id += 'anonymous_'
        else:
            id += mtools.getAuthenticatedMember().getUserName()+'_'
        id += self.REQUEST.environ.get('REMOTE_ADDR', 'unknown_ip')+'_'
        id += '%3.3d' % randrange(999)
        return id

    security.declarePrivate('_decode_id')
    def _decode_id(self, id=''):
        """ return a tuple (user,ip,date) or None for bad id """
        m=match(r'^(\d+)_([^_]+)_([^_]+)_\d+$', id)
        if m is None:
            return None, None, None
        d=time.strptime(m.group(1), '%y%m%d%H%M%S')
        user=m.group(2)
        ip=m.group(3)
        return (user,ip, d)
    
    security.declarePrivate('notify_modified')
    def notify_modified(self):
        self._p_changed = 1        
        # tell to the CMF that something changed
        self.notifyModified()


InitializeClass(CollectorDocument)

def addCollectorDocument(dispatcher, id, REQUEST=None, **kw):
    """Add a Collector Document"""
    ob = CollectorDocument(id, **kw)
    return BaseDocument_adder(dispatcher, id, ob, REQUEST=REQUEST)

#EOF