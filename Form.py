# $Id$
# an html form generator

### import
from re import match
from Globals import InitializeClass
from ExtensionClass import Base
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

### class
class Form(Base):
    "Form class"

    security = ClassSecurityInfo()
    #security_* used to raise an exception in skin 
    security.declarePrivate('assert_form_private')
    def assert_form_private(self):
        pass

    security.declareProtected(View, 'assert_form_view')
    def assert_form_view(self):
        pass

    security.declareProtected(ModifyPortalContent, 'assert_form_modify')
    def assert_form_modify(self):
        pass

    # DEFINITION OF FIELDS
    types = ('title', 'separator', 'comment',
             'string', 'email', 'identifier', 'string_ro', 'phone',
             'date', 'url', 'password',
             'int', 'float',
             'text', 'file',
             'checkbox', 'radio', 'selection',
             'submit', 'reset', 'hidden')

    # field attributes
    # title__, id__, type__ and submit__ are automaticly added
    field_attr = {}
    field_attr['string']=('label__', 'size__', 'maxlength__',
                           'value__', 'required__', 'join__')
    field_attr['identifier']=field_attr['email']=field_attr['phone']= \
                              field_attr['int']=field_attr['float']= \
                              field_attr['url']=field_attr['password']= \
                              field_attr['date']= \
                              field_attr['string']
    field_attr['string_ro']=('label__', 'value__', 'join__')
    field_attr['reset']=field_attr['submit']= field_attr['string_ro']
    field_attr['hidden']=('value__',)
    field_attr['title']=('label__', 'join__')
    field_attr['separator']=field_attr['comment']=field_attr['title']
    field_attr['file']=('label__', 'value__', 'maxlength__', 'required__', 'join__')
    field_attr['text']=('label__', 'cols__', 'rows__', 'value__',
                         'required__', 'join__')
    field_attr['checkbox']=('label__', 'checked__', 'required__', 'join__')
    field_attr['radio']=('label__', 'mvalue__', 'checked__', 'join__')
    field_attr['selection']=('label__', 'mvalue__', 'checked__',
                              'multiple__', 'size__', 'required__', 'join__')

    def __init__(self, id):
        "construtor, you can use post_init to setup zpt stuff"
        self.id = id

        # creation of internal fields
        self.add_field('title__', type='title', label='_form_field_edit_')
        self.add_field('id__', type='string_ro', label='Id:', join='on')
        self.add_field('type__', type='string_ro', label='_form_type_')
        self.add_field('label__', type='string', label='_form_label_')
        self.add_field('size__', type='int', label='_form_size_')
        self.add_field('cols__', type='int', label='_form_cols_')
        self.add_field('rows__', type='int', label='_form_rows_')
        self.add_field('maxlength__', type='int', label='_form_max_length_')
        self.add_field('required__', type='checkbox', label='_form_required_')
        self.add_field('checked__', type='string', label='_form_checked_')
        self.add_field('value__', type='string', label='_form_value_')
        self.add_field('mvalue__', type='text', label='_form_values_',
                        cols=40, rows=5)
        self.add_field('multiple__', type='checkbox', label='_form_mulitple_')
        self.add_field('submit__', type='submit', label='_form_bt_change_',
                   value='editField:method')
        self.add_field('join__', type='checkbox', label='_form_join_with_next_')

    # ZPT default
    _macros_pt='Form_macros'
    _view_pt='Form_view'
    _msg_pt='Form_msg'
    _editForm_pt='Form_editForm'
    _editField_pt='Form_editField'
    
    security.declarePrivate('post_init')
    def post_init(self, **kw):
        """ setup tpl stuff
        view_pt: used to display the form + error input
        msg_pt: when action is performed
        editForm_pt: edit a form (add/move/rm field)
        editField_pt: edit a field (properties)
        """
        self._view_pt=kw.get('view_pt', self._view_pt)
        self._msg_pt=kw.get('msg_pt', self._msg_pt)
        self._editForm_pt=kw.get('editForm_pt', self._editForm_pt)
        self._editField_pt=kw.get('editField_pt', self._editField_pt)
        self._macros_pt=kw.get('macros_pt', self._macros_pt)

    security.declarePrivate('_display_zpt')
    def _display_zpt(self, zpt_name, **kw):
        # call zpt_name
        zpt = self.restrictedTraverse(zpt_name)
        self._v_macros = self.restrictedTraverse(self._macros_pt)
        return zpt(**kw)

    ###
    security.declareProtected(View, 'action')
    def action(self, **kw):
        "this method should be rewrite by child"
        return self._display_zpt(self._msg_pt, **kw)

    security.declareProtected(View, 'validator')
    def validator(self, form):
        "this method should be rewrite by child, should return error str"
        return None

    security.declarePrivate('notify_modified')
    def notify_modified(self):
        self._p_changed = 1
        
    ### ZOPE ACCESSORS / CONSTRUCTORS
    security.declareProtected(View, 'index_html')
    def index_html(self, **kw):
        "default view"
        return self.view(**kw)

    security.declareProtected(View, 'view')
    def view(self, **kw):
        "default view"
        self._set_status()
        status,err=self.check_form()
        if status == 'valid_form':
            return self.action(**kw)
        if err:
            self._set_status(err)
        return self._display_zpt(self._view_pt, **kw)

    security.declareProtected(ModifyPortalContent, 'editForm')
    def editForm(self, **kw):
        "edit a form"
        self._set_status()
        status,err=self.check_form()
        if status == 'not_yet_submited':
            return self._display_zpt(self._editForm_pt, **kw)
        elif status == 'bad_fields':
            self._set_status(err)
        return self._display_zpt(self._editForm_pt, **kw)

    security.declareProtected(ModifyPortalContent, 'editField')
    def editField(self, **kw):
        "edit field form"
        form = self.REQUEST.form
        id = form.get('f_id') or form.get('id__')
        if not self.fields.has_key(id):
            return self._display_zpt(self._editForm_pt, **kw) # wrong id
        self._set_current_form(self.fields[id]['type'])
        status,err = self.check_form()
        if status == 'not_yet_submited':
            # display form
            id = form.get('f_id')
            # setting REQUEST.form
            for f in self.field_attr[ self.fields[id]['type'] ]:
                if f == 'mvalue__':
                    form[f]=self._mvalue_to_str(self.fields[id].get('mvalue'))
                else:
                    form[f]=self.fields[id].get(f[:-2] ,None)
            form['id__']=id
            form['type__']=self.fields[id]['type']
            return self._display_zpt(self._editField_pt, **kw)

        # process form
        id = form.get('id__')
        if status == 'bad_fields':
            self._set_status(err)
            return self._display_zpt(self._editField_pt, **kw)
        # setting new values_ and return to edit form
        extra={}
        for f in self.field_attr[ self.fields[id]['type'] ]:
            extra[f[:-2]] = form.get(f)

        self.add_field(id, **extra)
        self._set_current_form(None)
        return self._display_zpt(self._editForm_pt, **kw)

    security.declareProtected(ModifyPortalContent, 'addField')
    def addField(self, **kw):
        "add a field"
        id = self.REQUEST.form.get('id')
        t = self.REQUEST.form.get('type')
        self.add_field(id, type=t)
        self.REQUEST.form['f_id']=id
        return self.editField(**kw)

    security.declareProtected(ModifyPortalContent, 'delField')
    def delField(self, **kw):
        "remove a field"
        f_id = self.REQUEST.form.get('f_id')
        if f_id and type(f_id) is type([]):
            for id in f_id:
                self.del_field(id)
        else:
            self.del_field(f_id)
        return self._display_zpt(self._editForm_pt, **kw)

    security.declareProtected(ModifyPortalContent, 'moveFieldUp')
    def moveFieldUp(self, **kw):
        "move a field up"
        f_id = self.REQUEST.form.get('f_id')
        if f_id and type(f_id) is type([]):
            for id in f_id:
                self.move_field(id, 'up')
        else:
            self.move_field(f_id, 'up')
        return self._display_zpt(self._editForm_pt, **kw)

    security.declareProtected(ModifyPortalContent, 'moveFieldDown')
    def moveFieldDown(self, **kw):
        "move a field down"
        f_id = self.REQUEST.form.get('f_id')
        if f_id and type(f_id) is type([]):
            f_id.reverse()
            for id in f_id:
                self.move_field(id, 'down')
        else:
            self.move_field(f_id, 'down')
        return self._display_zpt(self._editForm_pt, **kw)

    security.declareProtected(ModifyPortalContent, 'dumpFields')
    def dumpFields(self):
        "dump fields"
        s = ''
        for f in self.fields_list:
            params=''
            for p in self.fields[f].keys():
                v = self.fields[f].get(p, None)
                if not v:
                    continue
                if p == 'mvalue':
                    v = self._mvalue_to_str(v,0)
                params += '%s=\'%s\'' % (p, v) +', '
            if params:
                params = params[:-2]
            s += '        self.add_field(\''+f+'\', '+params+')\n'
        return s

    security.declarePrivate('_set_current_form')
    def _set_current_form(self, mode):
        self.REQUEST.other['form_mode__']=mode

    security.declarePrivate('_get_current_form')
    def _get_current_form(self):
        return self.REQUEST.other.get('form_mode__', None)

    security.declarePrivate('_set_status')
    def _set_status(self, s=None):
        self.REQUEST.other['form_status'] = s


    ### ZPT ACCESSORS / CONSTRUCTORS
    security.declareProtected(View, 'getFList')
    def getFList(self, only_data=0):
        # return a list of field ids depending on the current form
        form_name=self._get_current_form()
        if form_name and self.field_attr.has_key(form_name):
            return ('title__', 'id__', 'type__') + \
                   self.field_attr[form_name] + ('submit__',)
        if only_data:
            l=[]
            for f in self.fields_list:
                if self.fields[f]['type'] not in \
                   ('submit', 'separator', 'title', 'comment', 'reset'):
                    l.append(f)
            return l
        return self.fields_list

    security.declareProtected(View, 'getVList')
    def getVList(self, f_name):
        # return the list of value for a field
        if not self.fields[f_name].has_key('mvalue'):
            return (f_name)
        l = self.fields[f_name]['mvalue'].keys()
        l.sort()
        return l

    security.declareProtected(View, 'getV')
    def getV(self, f, k, default=None, as_list=None):
        # return the value of field f on request
        form=self.REQUEST.form
        v=form.get(f)                   # form first
        if not v and len(form)==0:
            v=self.fields[f].get(k)     # no form try object value
        if not v and len(form)==0:      # no form no object value try default
            v=default
        if as_list:
            if type(v) is not type([]):
                v = [v,]
        return v

    security.declareProtected(View, 'getNbSlot')
    def getNbSlot(self, f_name):
        # return the number of cels used by a field
        t = self.fields[f_name]['type']
        if t in ('submit', 'reset', 'separator', 'title', 'comment'):
            n=1
        elif t in ('hidden', ):
            n=0
        else:
            n=2
        return n

    security.declareProtected(View, 'getFMacro')
    def getFMacro(self,f_name):
        # return the zpt macro associated with the field
        t = self.fields[f_name]['type']
        if t in ('string', 'identifier', 'email', 'int', 'float', 'phone', \
                  'url', 'date'):
            return self._v_macros.macros['string']
        return self._v_macros.macros[t]


    security.declareProtected(View, 'getLabel')
    def getLabel(self,f_name, multiple=0):
        # label starting with '_' are localized
        if multiple:
            if self.fields[f_name].get('mvalue'):
                label = self.fields[f_name]['mvalue'].get(multiple, '')
            else:
                label = multiple
        else:
            label = self.fields[f_name].get('label', '')
        if not len(label) or label[0]!='_':
            return label
        return self.portal_messages(label)

    security.declareProtected(View, 'isSelected')
    def isSelected(self, f=None, v=None):
        # check if f_name is selected
        if not f or not v:
            return 0
        v_ = self.REQUEST.form.get(f)
        if not v_:
            return 0
        if type(v_) is type([]):
            return v in v_
        return v_ == v

    security.declareProtected(View, 'getRows')
    def getRows(self):
        # return a list of rows
        rows = []
        join = 0
        nb_cols = []
        max_cols = max_rows = 0
        for f in self.getFList():
            if not join:
                rows.append([f,])
                nb_cols.append(self.getNbSlot(f))
                max_rows = max_rows + 1
            else:
                rows[-1].append(f)
                nb_cols[-1] = nb_cols[-1] + self.getNbSlot(f)
                join = 0
            if self.fields[f].get('join'):
                join = 1
            if nb_cols[-1] > max_cols:
                max_cols = nb_cols[-1]

        span = {}
        for r in rows:
            for f in r:
                span[f]=0
            span[f] = max_cols - nb_cols[rows.index(r)] + 1
        self.span = span
        return rows


    ### INTERNAL ACCESSORS / CONSTRUCTORS
    security.declarePrivate('add_field')
    def add_field(self, id, **extra):
        # add or modify field to the form
        if not id:
            return
        if not hasattr(aq_base(self), 'fields'):
            self.fields = {}
            self.fields_list = []
        if not self.fields.has_key(id):
            self.fields[id]={}
            if id.find('__') == -1:
                self.fields_list.append(id)

        f=self.fields[id]               # setting attributes
        for k in extra.keys():
            if k == 'mvalue':
                f[k]=self._str_to_mvalue(extra[k])
            else:
                f[k]=extra[k]

        t=f.get('type')                 #setting default type
        if not t in self.types:
            f['type']='string'
        self.notify_modified()
        
    security.declarePrivate('del_field')
    def del_field(self, id):
        # delete a field
        if not id or not id in self.fields_list:
            return
        self.fields_list.remove(id)
        del self.fields[id]
        self.notify_modified()

    security.declarePrivate('move_field')
    def move_field(self, id, direction='up'):
        # move a field up or down
        if not id or not id in self.fields_list:
            return
        pos=self.fields_list.index(id)
        if direction=='down':
            self.fields_list.remove(id)
            self.fields_list.insert(pos+1, id)
        else:
            self.fields_list.remove(id)
            self.fields_list.insert(pos-1, id)
        self.notify_modified()

    security.declarePrivate('check_form')
    def check_form(self ):
        # check all the fields of a form and return a status and msg
        form = self.REQUEST.form
        mcat = self.portal_messages
        locale = mcat.get_selected_language()
        if not ( form.get('is_form_submitted') or form.get('is_form_setted') ):
            if not len(self.fields_list):
                msg = mcat('_form_is_empty_')
            else:
                msg = ''
            return ('not_yet_submited', msg)
        msg=''
        bf=[]
        for f in self.getFList():
            err = self.check_field(f, form.get(f), locale)
            if err:
                err_l10n = mcat(err)
                if err_l10n != err:
                    err = err_l10n % f
                else:
                    err = '['+f+'] '+err
                msg = msg + err + ', '
                bf.append(f)
        form['error__'] =  bf
        if not msg:
            msg = self.validator(form)

        if msg:
            err_l10n = mcat('_field_error_')
            return ('bad_fields', err_l10n + ' ' + msg[:-2] +'.')

        if form.get('is_form_setted'):
            return ('setted_form', None)

        return ('valid_form', 'Congratulation')

    security.declarePrivate('check_field')
    def check_field(self, id, v, locale='en'):
        # check input and set default value
        # assume id is valid
        f = self.fields[id]
        t = f['type']
        err=None

        if not v and f.get('required', 0):
            err='_field_is_required_'
        elif not v:
            pass
        elif t == 'string':
            max_len = f.get('maxlength', 128)
            if len(v) > max_len:
                err = '_field_is_too_long_'
        elif t == 'email':
            if not match(r'^(\w(\.|\-)?)+@(\w(\.|\-)?)+\.[A-Za-z]{2,4}$', v):
                err = '_field_email_invalid_'
        elif t == 'int':
            if not match(r'^(\-)?[0-9]+$', v):
                err = '_field_int_invalid_'
        elif t == 'float':
            if not match(r'^[0-9]+((\.|\,)[0-9]+)?$', v):
                err= '_field_float_invalid_'
        elif t == 'phone':
            if not match(r'^[\(\)0-9\t\ \-\.\+]{6,26}$', v):
                err = '_field_phone_invalid_'
        elif t == 'checkbox':
            pass
        elif t == 'hidden':
            pass
        elif t == 'string_ro':
            _v = self.fields[id].get('value')
            if _v and (_v != v):
                err = '_field_is_read_only_'
        elif t == 'identifier':
            if not match(r'^[a-zA-Z]\w*$', v):
                err = '_field_id_invalid_'
        elif t == 'text':
            pass
        elif t == 'selection':
            if type(v) is type([]):
                if not f.get('multiple'):
                    err = '_field_multiselect_invalid_'
                for vv in v:
                    if vv not in f['mvalue'].keys():
                        err = '_field_multiselect_invalid_'
                        break
            elif v not in f['mvalue'].keys():
                err = '_field_selection_invalid_'
        elif t == 'radio':
            if v not in f['mvalue'].keys():
                err = '_field_selection_invalid_'
        elif t == 'date':
            if locale == 'en':
                if not match(r'^((0?[1-9])|(1[0-2]))/((0?[1-9])|([12][0-9])|(3[01]))/[0-9]{4,4}$', v):
                    err = '_field_date_invalid_'
            elif locale == 'fr':
                if not match(r'^((0?[1-9])|([12][0-9])|(3[01]))/((0?[1-9])|(1[0-2]))/[0-9]{4,4}$', v):
                    err = '_field_date_invalid_'
            elif not match(r'^[0-9]?[0-9]/[0-9]?[0-9]/[0-9]{4,4}$', v):
                err = '_field_date_invalid_'
        elif t == 'url':
            if not match(r'^(http://)?([\w\~](\:|\.|\-|\/|\?|\=)?){2,}$', v):
                err = '_field_url_invalid_'
        elif t == 'password':
            pass
        elif t == 'file':
            if not v.filename and f.get('required',0):
                err = '_field_is_required_'
            elif v.filename:
                ml = int(f.get('maxlength', '0'))
                if v.read(1) == "":
                    err = '_field_empty_file_'
                    self.REQUEST.form[id] = v.filename
                elif ml:
                    if len(v.read(ml + 1)) == ml + 1:
                        err = '_field_too_big_file_'
                        self.REQUEST.form[id]=v.filename
                v.seek(0)

        return err

    security.declarePrivate('_mvalue_to_str')
    def _mvalue_to_str(self, m, multiline=1):
        # convert a mvalue dico into a string
        if type(m) is not type({}) :
            return ''
        str = ''
        keys = m.keys()
        keys.sort()
        for k in keys:
            str = str + k + ' | ' + m[k]
            if multiline:
                str += '\n'
            else:
                str += '\\n'
        return str

    security.declarePrivate('_str_to_mvalue')
    def _str_to_mvalue(self, s):
        # convert a mvalue string to dico
        mvalue = {}
        lines = s.split('\n')
        if not len(lines):
            return mvalue
        for l in lines:
            t = l.split('|')
            if len(t[0].strip()) < 1:
                continue
            if len(t) == 1:
                t.append(t[0])
            elif len(t) != 2:
                continue
            mvalue[t[0].strip()]=t[1].strip()
        return mvalue

    security.declarePrivate('get_values')
    def get_values(self, no_fd=1):
        # return dico field:value
        v = {}
        form = self.REQUEST.form
        for f in self.getFList(1):
            if no_fd and self.fields[f]['type'] == 'file':
                v[f] = form.get(f).filename
            else:
                v[f] = form.get(f)
        return v

    security.declarePrivate('set_values')
    def set_values(self, values):
        # set form values from dico
        pp = self.REQUEST.form.get('pp')
        self.REQUEST.form = values
        self.REQUEST.form['is_form_setted'] = 'yes'
        self.REQUEST.form['pp'] = pp
    

InitializeClass(Form)
# EOC Form
