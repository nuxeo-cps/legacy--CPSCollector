# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# $Id$
"""
The Form class is an HTML form generator.
This is a very simple 'Formulator like' tool. A Form object displays a web
form until input are correct, then it executes the action method.
The Form is editable TTW.
"""

# import
from re import match
from Globals import InitializeClass
from ExtensionClass import Base
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

# class
class Form(Base):
    """A Form knows how to render and validate its fields and
    it knows how to edit itself using ... itself.
    _action and _validator methods should be overriden in subclasses
    """

    # ZPT default
    _macros_pt = 'Form_macros'
    _view_pt = 'Form_view_pt'
    _action_pt = 'Form_action'
    _editForm_pt = 'Form_editForm'
    _editField_pt = 'Form_editField_pt'

    # Type of fields
    types = ('title', 'separator', 'comment',
             'string', 'email', 'identifier', 'string_ro', 'phone',
             'date', 'url', 'password',
             'int', 'float',
             'text', 'file',
             'checkbox', 'radio', 'vradio', 'selection',
             'submit', 'reset', 'hidden')

    # Fields attributes that describe fields
    # title__, id__, type__ and submit__ are automaticly added
    field_attr = {}
    field_attr['string'] = ('label__', 'size__', 'maxlength__',
                            'value__', 'required__', 'join__')
    field_attr['identifier'] = field_attr['email'] = field_attr['phone'] = \
        field_attr['int'] = field_attr['float'] = \
        field_attr['url'] = field_attr['password'] = \
        field_attr['date'] = field_attr['string']
    field_attr['string_ro'] = ('label__', 'value__', 'join__')
    field_attr['reset'] = field_attr['submit'] = field_attr['string_ro']
    field_attr['hidden'] = ('value__',)
    field_attr['title'] = ('label__', 'join__')
    field_attr['separator'] = field_attr['comment'] = field_attr['title']
    field_attr['file'] = ('label__', 'value__', 'maxlength__', 'required__',
                          'join__')
    field_attr['text'] = ('label__', 'cols__', 'rows__', 'value__',
                          'required__', 'join__')
    field_attr['checkbox'] = ('label__', 'checked__', 'required__', 'join__')
    field_attr['radio'] = ('label__', 'mvalue__', 'checked__', 'join__')
    field_attr['vradio'] = ('label__', 'mvalue__', 'checked__', 'join__')
    field_attr['selection'] = ('label__', 'mvalue__', 'checked__',
                               'multiple__', 'size__', 'required__', 'join__')

    security = ClassSecurityInfo()

    def __init__(self, id):
        """Construtor"""
        self.id = id
        # creation of internal fields ending with '__'
        self.add_field('title__', type='title',
                       label='collector_form_field_edit')
        self.add_field('id__', type='string_ro', label='Id:', join='on')
        self.add_field('type__', type='string_ro', label='collector_form_type')
        self.add_field('label__', type='text', label='collector_form_label',
                       cols=40, rows=2)
        self.add_field('size__', type='int', label='collector_form_size')
        self.add_field('cols__', type='int', label='collector_form_cols')
        self.add_field('rows__', type='int', label='collector_form_rows')
        self.add_field('maxlength__', type='int',
                       label='collector_form_max_length')
        self.add_field('required__', type='checkbox',
                       label='collector_form_required')
        self.add_field('checked__', type='string',
                       label='collector_form_checked')
        self.add_field('value__', type='string',
                       label='collector_form_value')
        self.add_field('mvalue__', type='text',
                       label='collector_form_values', cols=40, rows=5)
        self.add_field('multiple__', type='checkbox',
                       label='collector_form_mulitple')
        self.add_field('submit__', type='submit',
                       value='Form_editField:method',
                       label='collector_button_change')
        self.add_field('join__', type='checkbox',
                       label='collector_form_join_with_next')

    security.declareProtected(ModifyPortalContent, 'personalizeZPT')
    def personalizeZPT(self, macros=None, view=None, action=None,
                       editForm=None, editField=None):
        """Personnalize the five hardcoding zpt for duplicate
        use of the class"""

        if macros is None or macros == '':
            self._macros_pt = 'Form_macros'
        else:
            self._macros_pt = macros

        if view is None or view == '':
            self._view_pt = 'Form_view_pt'
        else:
            self._view_pt = view

        if action is None or action == '':
            self._action_pt = 'Form_action'
        else:
            self._action_pt = action

        if editForm is None or editForm == '':
            self._editForm_pt = 'Form_editForm'
        else:
            self._editForm_pt = editForm

        if editField is None or editField == '':
            self._editField_pt = 'Form_editField_pt'
        else:
            self._editField_pt = editField

    # WEB INTERFACE --------------------------------------------------
    security.declareProtected(ModifyPortalContent, 'dumpFields')
    def dumpFields(self):
        """Dump python source that creates the form"""
        s = ''
        for f in self.fields_list:
            params = ''
            for p in self.fields[f].keys():
                v = self.fields[f].get(p, None)
                if not v:
                    continue
                if p == 'mvalue':
                    v = self._mvalue_to_str(v,0)
                params += '%s=\'%s\'' % (p, v) + ', '
            if params:
                params = params[:-2]
            s += '        self.add_field(\''+f+'\', '+params+')\n'
        return s

    # ZTP INTERFACE --------------------------------------------------
    #   View helper --------------------------------------------------
    security.declareProtected(View, 'process_view')
    def process_view(self, **kw):
        # Return a zpt_name to be displayed
        self._set_status()
        status, err = self._check_form()
        if status == 'valid_form':
            self._action(**kw)
            return self._action_pt
        if err:
            self._set_status(err)
        return self._view_pt

    security.declareProtected(ModifyPortalContent, 'process_edit_field')
    def process_edit_field(self, **kw):
        # The field edition page use its own Form fields
        form = self.REQUEST.form
        id = form.get('f_id') or form.get('id__')
        if not self.fields.has_key(id):
            return self._editForm_pt     # wrong id
        self._set_current_form(self.fields[id]['type'])
        status,err = self._check_form()
        if status == 'not_yet_submitted':
            # display form
            id = form.get('f_id')
            # setting REQUEST.form
            for f in self.field_attr[self.fields[id]['type']]:
                if f == 'mvalue__':
                    form[f] = self._mvalue_to_str(self.fields[id].get('mvalue'))
                else:
                    form[f] = self.fields[id].get(f[:-2] ,None)
            form['id__'] = id
            form['type__'] = self.fields[id]['type']
            return self._editField_pt
        # process form
        id = form.get('id__')
        if status == 'bad_fields':
            self._set_status(err)
            return self._editField_pt
        # setting new values_ and return to edit form
        extra = {}
        for f in self.field_attr[self.fields[id]['type']]:
            extra[f[:-2]] = form.get(f)
        self.add_field(id, **extra)
        self._set_current_form(None)
        return self._editForm_pt


    #   Fields Setters -----------------------------------------------
    security.declareProtected(ModifyPortalContent, 'add_field')
    def add_field(self, id, **extra):
        # Add or modify field to the form
        if not id:
            return
        if not hasattr(aq_base(self), 'fields'):
            self.fields = {}
            self.fields_list = []
        if not self.fields.has_key(id):
            self.fields[id] = {}
            if id.find('__') == -1:
                self.fields_list.append(id)
        f = self.fields[id]               # setting attributes
        for k in extra.keys():
            if k == 'mvalue':
                f[k] = self._str_to_mvalue(extra[k])
            else:
                f[k] = extra[k]
        t = f.get('type')                 #setting default type
        if not t in self.types:
            f['type'] = 'string'
        self._notify_modified()
        return 1

    security.declareProtected(ModifyPortalContent, 'del_field')
    def del_field(self, id):
        # Delete a field
        if not id or not id in self.fields_list:
            return
        self.fields_list.remove(id)
        del self.fields[id]
        self._notify_modified()
        return 1

    security.declareProtected(ModifyPortalContent, 'del_fields')
    def del_fields(self, ids):
        # Delete many fields
        if ids and type(ids) is type([]):
            ret = 1
            for id in ids:
                ret = self.del_field(id) and ret
        else:
            ret = self.del_field(ids)
        return ret

    security.declareProtected(ModifyPortalContent, 'move_field')
    def move_field(self, id, direction='up'):
        # Move a field up or down
        if not id or not id in self.fields_list:
            return
        pos = self.fields_list.index(id)
        if direction == 'down':
            self.fields_list.remove(id)
            self.fields_list.insert(pos + 1, id)
        else:
            self.fields_list.remove(id)
            self.fields_list.insert(pos - 1, id)
        self._notify_modified()
        return 1

    security.declareProtected(ModifyPortalContent, 'move_fields')
    def move_fields(self, ids, direction='up'):
        # Move many fields
        if ids and type(ids) is type([]):
            ret = 1
            if direction == 'down':
                ids.reverse()
            for id in ids:
                ret = self.move_field(id, direction) and ret
        else:
            ret = self.move_field(ids, direction)
        return ret


    #   Fields accessor ----------------------------------------------
    security.declareProtected(View, 'getFList')
    def getFList(self, only_data=0):
        # Return a list of field ids depending on the current form
        form_name = self._get_current_form()
        if form_name and self.field_attr.has_key(form_name):
            return ('title__', 'id__', 'type__') + \
                   self.field_attr[form_name] + ('submit__',)
        if only_data:
            l = []
            for f in self.fields_list:
                if self.fields[f]['type'] not in \
                   ('submit', 'separator', 'title', 'comment', 'reset'):
                    l.append(f)
            return l
        return self.fields_list

    security.declareProtected(View, 'getVList')
    def getVList(self, f_name):
        # Return the list of value for a field
        if not self.fields[f_name].has_key('mvalue'):
            return (f_name)
        l = self.fields[f_name]['mvalue'].keys()
        l.sort()
        return l

    security.declareProtected(View, 'getV')
    def getV(self, f, k, default=None, as_list=None):
        # Return the value of field f on request
        form = self.REQUEST.form
        v = form.get(f)                   # form first
        if not v and len(form) == 0:
            v = self.fields[f].get(k)     # no form try object value
        if not v and len(form) == 0:      # no form no object value try default
            v = default
        if as_list:
            if type(v) is not type([]):
                v = [v,]
        return v

    security.declareProtected(View, 'getNbSlot')
    def getNbSlot(self, f_name):
        # Return the number of cels used by a field
        t = self.fields[f_name]['type']
        if t in ('submit', 'reset', 'separator', 'title', 'comment', 'vradio'):
            n = 1
        elif t in ('hidden',):
            n = 0
        else:
            n = 2
        return n

    security.declareProtected(View, 'getFMacro')
    def getFMacro(self, f_name):
        # Return the zpt macro associated with the field
        t = self.fields[f_name]['type']
        if t in ('string', 'identifier', 'email', 'int', 'float', 'phone',
                 'url', 'date'):
            t = 'string'
##        """
##        if not hasattr(self, '_v_macros'):
##            self._v_macros = self.restrictedTraverse(self._macros_pt)
##        """
        return self.restrictedTraverse(self._macros_pt).macros[t]
        
    security.declareProtected(View, 'getLabel')
    def getLabel(self,f_name, multiple=0):
        # Label starting with '_' are localized
        if multiple:
            if self.fields[f_name].get('mvalue'):
                label = self.fields[f_name]['mvalue'].get(multiple, '')
            else:
                label = multiple
        else:
            label = self.fields[f_name].get('label', '')
        if not len(label) or label[0] != '_':
            return label
        return self.Localizer.cpscollector(label)

    security.declareProtected(View, 'isSelected')
    def isSelected(self, f=None, v=None):
        # Check if f_name is selected
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
        # Return a list of rows
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
                span[f] = 0
            span[f] = max_cols - nb_cols[rows.index(r)] + 1
        if span != getattr(self, 'span', None):
            self.span = span
        return rows

    #   Security Stuff used to raise an exception in skin ------------
    security.declarePrivate('assert_form_private')
    def assert_form_private(self):
        pass

    security.declareProtected(View, 'assert_form_view')
    def assert_form_view(self):
        pass

    security.declareProtected(ModifyPortalContent, 'assert_form_modify')
    def assert_form_modify(self):
        pass


    # INTERNAL -------------------------------------------------------
    #   Form validation ----------------------------------------------
    security.declarePrivate('_validator')
    def _validator(self, form):
        """This method should be overriden in a subclass
        Its purpose is to validate the whole form
        Called after the _check_form method"""
        pass

    security.declarePrivate('_check_form')
    def _check_form(self):
        """Check all the fields of a form and return a status and msg """
        form = self.REQUEST.form
        locale = self.Localizer.cpscollector.get_selected_language()
        if not (form.get('is_form_submitted') or form.get('is_form_setted')):
            if not len(self.fields_list):
                msg = self.Localizer.cpscollector('collector_empty_form')
            else:
                msg = ''
            return ('not_yet_submitted', msg)
        msg = ''
        bf = []
        for f in self.getFList():
            err = self._check_field(f, form.get(f), locale)
            if err:
                err_l10n = self.Localizer.cpscollector(err)
                if err_l10n != err:
                    err = err_l10n % f
                else:
                    err = '[' + f + '] ' + err
                msg = msg + err + ', '
                bf.append(f)
        form['error__'] =  bf
        if not msg:
            msg = self._validator(form)
        if msg:
            err_l10n = self.Localizer.cpscollector('collector_field_error')
            return ('bad_fields', err_l10n + ' ' + msg[:-2] +'.')
        if form.get('is_form_setted'):
            return ('setted_form', msg)
        return ('valid_form', 'Congratulation')

    security.declarePrivate('_check_field')
    def _check_field(self, id, v, locale='en'):
        """Check input and set default value
        assume id is valid """
        f = self.fields[id]
        t = f['type']
        err = None

        if not v and f.get('required', 0):
            err = 'collector_field_required'
        elif not v:
            pass
        elif t == 'string':
            max_len = f.get('maxlength', 128)
            if len(v) > max_len:
                err = 'collector_field_too_long'
        elif t == 'email':
            if not match(r'^(\w(\.|\-)?)+@(\w(\.|\-)?)+\.[A-Za-z]{2,4}$', v):
                err = 'collector_field_email_invalid'
        elif t == 'int':
            if not match(r'^(\-)?[0-9]+$', v):
                err = 'collector_field_int_invalid'
        elif t == 'float':
            if not match(r'^[0-9]+((\.|\,)[0-9]+)?$', v):
                err = 'collector_field_float_invalid'
        elif t == 'phone':
            if not match(r'^[\(\)0-9\t\ \-\.\+]{6,26}$', v):
                err = 'collector_field_phone_invalid'
        elif t == 'checkbox':
            pass
        elif t == 'hidden':
            pass
        elif t == 'string_ro':
            _v = self.fields[id].get('value')
            if _v and (_v != v):
                err = 'collector_field_read_only'
        elif t == 'identifier':
            if not match(r'^[a-zA-Z]\w*$', v):
                err = 'collector_field_id_invalid'
        elif t == 'text':
            pass
        elif t == 'selection':
            if type(v) is type([]):
                if not f.get('multiple'):
                    err = 'collector_field_multiselect_invalid'
                for vv in v:
                    if vv not in f['mvalue'].keys():
                        err = 'collector_field_multiselect_invalid'
                        break
            elif v not in f['mvalue'].keys():
                err = 'collector_field_selection_invalid'
        elif t == 'radio':
            if v not in f['mvalue'].keys():
                err = 'collector_field_selection_invalid'
        elif t == 'vradio':
            if v not in f['mvalue'].keys():
                err = 'collector_field_selection_invalid'
        elif t == 'date':
            if locale == 'en':
                if not match(r'^((0?[1-9])|(1[0-2]))/((0?[1-9])|([12][0-9])|(3[01]))/[0-9]{4,4}$', v):
                    err = 'collector_field_date_invalid'
            elif locale == 'fr':
                if not match(r'^((0?[1-9])|([12][0-9])|(3[01]))/((0?[1-9])|(1[0-2]))/[0-9]{4,4}$', v):
                    err = 'collector_field_date_invalid'
            elif not match(r'^[0-9]?[0-9]/[0-9]?[0-9]/[0-9]{4,4}$', v):
                err = 'collector_field_date_invalid'
        elif t == 'url':
            if not match(r'^(http://)?([\w\~](\:|\.|\-|\/|\?|\=)?){2,}$', v):
                err = 'collector_field_url_invalid'
        elif t == 'password':
            pass
        elif t == 'file':
            if not v.filename and f.get('required',0):
                err = 'collector_field_required'
            elif v.filename:
                ml = int(f.get('maxlength', '0'))
                if v.read(1) == "":
                    err = 'collector_field_empty_file'
                    self.REQUEST.form[id] = v.filename
                elif ml:
                    if len(v.read(ml + 1)) == ml + 1:
                        err = 'collector_field_file_too_big'
                        self.REQUEST.form[id] = v.filename
                v.seek(0)

        return err

    #   Misc  --------------------------------------------------------
    security.declarePrivate('_action')
    def _action(self, **kw):
        """This method should be overriden in a subclass"""
        pass

    security.declarePrivate('_get_values')
    def _get_values(self, no_fd=1):
        """Return dico field:value """
        v = {}
        form = self.REQUEST.form
        for f in self.getFList(1):
            if no_fd and self.fields[f]['type'] == 'file':
                v[f] = form.get(f).filename
            else:
                v[f] = form.get(f)
        return v

    security.declarePrivate('_set_values')
    def _set_values(self, values):
        """Set form values from dico"""
        pp = self.REQUEST.form.get('pp')
        self.REQUEST.form = values
        self.REQUEST.form['is_form_setted'] = 'yes'
        self.REQUEST.form['pp'] = pp

    security.declarePrivate('_notify_modified')
    def _notify_modified(self):
        self._p_changed = 1

    security.declarePrivate('_set_current_form')
    def _set_current_form(self, mode):
        self.REQUEST.other['form_mode__'] = mode

    security.declarePrivate('_get_current_form')
    def _get_current_form(self):
        return self.REQUEST.other.get('form_mode__', None)

    security.declarePrivate('_set_status')
    def _set_status(self, s=None):
        self.REQUEST.other['form_status'] = s

    security.declarePrivate('_mvalue_to_str')
    def _mvalue_to_str(self, m, multiline=1):
        """Convert a mvalue dico into a string"""
        if type(m) is not type({}):
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
        """Convert a mvalue string to dico"""
        i = 1
        mvalue = {}
        lines = s.split('\n')
        if not len(lines):
            return mvalue
        for l in lines:
            t = l.split('|')
            if len(t[0].strip()) < 1:
                continue
            if len(t) == 1: # pipe symbol not used
                t.append(t[0])
            elif len(t) != 2:
                continue
            mvalue[t[0].strip()] = t[1].strip()
        return mvalue


InitializeClass(Form)
# EOC Form
