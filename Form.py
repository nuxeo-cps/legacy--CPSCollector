# $Id$
# an html form generator

### import
import Globals
import ExtensionClass
from re import match

### class
class Form(ExtensionClass.Base):
    "Form class"
    # TEMPLATES

    # DEFINITION OF FIELDS
    types = ( 'title', 'separator', 'comment',
              'string', 'email', 'identifier', 'string_ro', 'phone',
              'date','url','password',
              'int','float', 
              'text','file', 
              'checkbox', 'radio', 'selection',
              'submit', 'reset', 'hidden' )

    # field attributes
    # title__, id__, type__ and submit__ are automaticly added
    field_attr = {} 
    field_attr['string']=( 'label__', 'size__', 'maxlength__',
                           'value__', 'required__', 'join__' )
    field_attr['identifier']=field_attr['email']=field_attr['phone']= \
                              field_attr['int']=field_attr['float']= \
                              field_attr['url']=field_attr['password']= \
                              field_attr['date']= \
                              field_attr['string']
    field_attr['string_ro']=( 'label__', 'value__', 'join__' )
    field_attr['reset']=field_attr['submit']= field_attr['string_ro']
    field_attr['hidden']=( 'value__', )
    field_attr['title']=( 'label__', 'join__' )
    field_attr['separator']=field_attr['comment']=field_attr['title']
    field_attr['file']=( 'label__', 'value__', 'maxlength__', 'required__', 'join__' )
    field_attr['text']=( 'label__', 'cols__', 'rows__', 'value__',
                         'required__', 'join__' )
    field_attr['checkbox']=( 'label__', 'checked__', 'required__', 'join__' )
    field_attr['radio']=( 'label__', 'mvalue__', 'checked__', 'join__' )
    field_attr['selection']=( 'label__', 'mvalue__', 'checked__',
                              'multiple__', 'size__', 'required__', 'join__' )

    def __init__( self, id, title ):
        "construtor"
        self.id = id
        self.title = title
        # creation of internal fields
        self.add_field( 'title__', type='title', label='Field edition:' )
        self.add_field( 'id__', type='string_ro', label='Id:', join='on' )
        self.add_field( 'type__', type='string_ro', label='Type:' )        
        self.add_field( 'label__', type='string', label='Label:' )
        self.add_field( 'size__', type='int', label='Size:' )
        self.add_field( 'cols__', type='int', label='Column:' )
        self.add_field( 'rows__', type='int', label='Rows:' )        
        self.add_field( 'maxlength__', type='int', label='Max Length:' )
        self.add_field( 'required__', type='checkbox', label='Required:' )
        self.add_field( 'checked__', type='string', label='Checked:' )
        self.add_field( 'value__', type='string', label='Value:' )
        self.add_field( 'mvalue__', type='text', label='Values:',
                        cols=40, rows=5 )
        self.add_field( 'multiple__', type='checkbox', label='Multiple:' )
        self.add_field( 'submit__', type='submit', label='Change',
                   value='editField:method' )
        self.add_field( 'join__', type='checkbox', label='Join with the next field')

    ### 
    def action(self, **kw):
        "this method should be rewrite by child"
        return self.CollectorDocument_view(**kw)

    def validator(self, form):
        "this method should be rewrite by child, should return error str"
        return None

    ### ZOPE ACCESSORS / CONSTRUCTORS
    def index_html( self, **kw ):
        "default view"
        return self.view(**kw)

    def view( self, **kw ):
        "default view"
        self._set_status()
        status,err=self.check_form()
        if status == 'not_yet_submited':
            return self.CollectorDocument_view(**kw)
        elif status == 'bad_fields':
            self._set_status( err )
            return self.CollectorDocument_view(**kw)
        return self.action(**kw)        

    def editForm( self, **kw ):
        "edit a form"
        self._set_status()
        status,err=self.check_form()
        if status == 'not_yet_submited':
            return self.Form_editForm(**kw)
        elif status == 'bad_fields':
            self._set_status(err)
        return self.Form_editForm(**kw)

    def editField( self, **kw ):
        "edit field form"
        form = self.REQUEST.form
        id = form.get( 'f_id' ) or form.get( 'id__' )
        if not self.fields.has_key( id ):
            return self.Form_editForm( **kw )  # wrong id
        self._set_current_form( self.fields[id]['type'] )
        status,err = self.check_form()
        if status == 'not_yet_submited':
            # display form
            id = form.get( 'f_id' ) 
            # setting REQUEST.form
            for f in self.field_attr[ self.fields[id]['type'] ]:
                if f == 'mvalue__':
                    form[f]=self._mvalue_to_str(self.fields[id].get('mvalue'))
                else:
                    form[f]=self.fields[id].get( f[:-2] ,None)
            form['id__']=id
            form['type__']=self.fields[id]['type']
            return self.Form_editField(**kw)

        # process form
        id = form.get( 'id__' )
        if status == 'bad_fields':
            self._set_status( err )
            return self.Form_editField( **kw )
        # setting new values_ and return to edit form
        extra={}
        for f in self.field_attr[ self.fields[id]['type'] ]:
            extra[f[:-2]] = form.get(f)

        self.add_field( id, **extra )
        self._set_current_form(None)
        return self.Form_editForm( **kw )
            
    def addField( self, **kw ):
        "add a field"
        id = self.REQUEST.form.get('id')
        t = self.REQUEST.form.get('type')
        self.add_field( id, type=t )
        self.REQUEST.form['f_id']=id
        return self.editField( **kw )
    
    def delField( self, **kw ):
        "remove a field"
        f_id = self.REQUEST.form.get('f_id')
        if f_id and type(f_id) is type([]):
            for id in f_id:
                self.del_field( id )
        else:
            self.del_field( f_id )
        return self.Form_editForm(**kw)
    
    def moveFieldUp( self, **kw ):
        "move a field up"
        f_id = self.REQUEST.form.get('f_id')
        if f_id and type(f_id) is type([]):
            for id in f_id:
                self.move_field( id, 'up' )
        else:
            self.move_field( f_id, 'up' )
        return self.Form_editForm(**kw)

    def moveFieldDown( self, **kw ):
        "move a field down"
        f_id = self.REQUEST.form.get('f_id')
        if f_id and type(f_id) is type([]):
            f_id.reverse()
            for id in f_id:
                self.move_field( id, 'down' )
        else:
            self.move_field( f_id, 'down' )
        return self.Form_editForm(**kw)

    def _set_current_form( self, mode ):
        self.REQUEST.other['form_mode__']=mode

    def _get_current_form( self ):
        return self.REQUEST.other.get('form_mode__', None )

    def _set_status( self, s=None ):
        self.REQUEST.other['form_status'] = s

    
    ### ZPT ACCESSORS / CONSTRUCTORS
    def getFList( self, only_data=0 ):
        # return a list of field ids depending on the current form
        form_name=self._get_current_form()
        if form_name and self.field_attr.has_key( form_name ):
            return ('title__', 'id__', 'type__' ) + \
                   self.field_attr[form_name] + ('submit__',)
        if only_data:
            l=[]
            for f in self.fields_list:
                if self.fields[f]['type'] not in \
                   ('submit','separator','title','comment','reset'):
                    l.append(f)
            return l
        return self.fields_list            

    def getVList( self, f_name):
        # return the list of value for a field
        if not self.fields[f_name].has_key('mvalue'):
            return (f_name)
        l = self.fields[f_name]['mvalue'].keys()
        l.sort()
        return l

    def getV( self, f, k, default=None):
        # return the value of field f on request
        form=self.REQUEST.form
        v=form.get(f)                   # form first
        if not v and len(form)==0:
            v=self.fields[f].get(k)     # no form try object value
        if not v and len(form)==0:      # no form no object value try default
            v=default
        return v

    def getNbSlot( self, f_name ):
        # return the number of cels used by a field
        t = self.fields[f_name]['type'] 
        if t in ( 'submit', 'reset', 'separator', 'title', 'comment' ):
            n=1
        elif t in ( 'hidden',  ):
            n=0
        else:
            n=2
        return n
    
    def getFMacro( self,f_name):
        # return the zpt macro associated with the field
        t = self.fields[f_name]['type']
        if t in ( 'string', 'identifier', 'email', 'int', 'float', 'phone', \
                  'url', 'date' ):
            return self.Form_macros.macros['string']
        return self.Form_macros.macros[t]

    def isSelected( self, f=None, v=None ):
        # check if f_name is selected
        if not f or not v:
            return 0
        v_ = self.REQUEST.form.get( f )
        if not v_:
            return 0
        if type( v_ ) is type( [] ):
            return v in v_
        return v_ == v

    def getRows( self ):
        # return a list of rows
        rows = []
        join = 0
        nb_cols = []
        max_cols = max_rows = 0
        for f in self.getFList():
            if not join:
                rows.append([f,])
                nb_cols.append( self.getNbSlot(f) )
                max_rows = max_rows + 1
            else:
                rows[-1].append( f )
                nb_cols[-1] = nb_cols[-1] + self.getNbSlot(f)
                join = 0
            if self.fields[f].get( 'join' ):
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
    def add_field( self, id, **extra ):
        # add or modify field to the form
        if not id:
            return
        if not hasattr(self, 'fields'):
            self.fields = {}
            self.fields_list = []
        if not self.fields.has_key( id ):
            self.fields[id]={}
            if id.find('__') == -1:
                self.fields_list.append(id)
    
        f=self.fields[id]               # setting attributes
        for k in extra.keys():
            if k == 'mvalue':
                f[k]=self._str_to_mvalue( extra[k] )
            else:
                f[k]=extra[k]

        t=f.get('type')                 #setting default type
        if not t in self.types:
            f['type']='string'
        self._p_changed = 1

    def del_field( self, id ):
        # delete a field
        if not id or not id in self.fields_list:
            return
        self.fields_list.remove(id)
        del self.fields[id]
        self._p_changed = 1

    def move_field( self, id, direction='up' ):
        # move a field up or down
        if not id or not id in self.fields_list:
            return
        pos=self.fields_list.index(id)
        if direction=='down':
            self.fields_list.remove(id)
            self.fields_list.insert( pos+1, id )
        else:
            self.fields_list.remove(id)
            self.fields_list.insert( pos-1, id )
        self._p_changed = 1

    def check_form( self  ):
        # check all the fields of a form and return a status and msg
        form = self.REQUEST.form
        if not form.get('is_form_submitted'):
            return ( 'not_yet_submited', '' )
        msg=''
        bf=[]
        for f in self.getFList( ):
            err = self.check_field( f, form.get(f) )
            if err:
               msg = msg + err + ', '
               bf.append( f )
        form['error__'] =  bf
        if not msg:
            msg = self.validator( form )            

        if msg:
            return ( 'bad_fields', 'ERROR: '+msg )

        return ( 'valid_form', 'Congratulation' )
        
    def check_field( self, id, v ):
        # check input and set default value
        # assume id is valid
        f = self.fields[id]
        t = f['type']
        err=None
        
        if not v and f.get('required',0):
            err='['+id+'] is required'
        elif not v:
            pass
        elif t == 'string':
            max_len = f.get('maxlength',128)
            if len(v) > max_len:
                err='['+id+'] is too long, maximum length is %d' %max_len
        elif t == 'email':
            if not match( r'^(\w(\.|\-)?)+@(\w(\.|\-)?)+\.[A-Za-z]{2,4}$',v):
                err='Invalid email format for ['+id+']'
        elif t == 'int':
            if not match( r'^(\-)?[0-9]+$', v):
                err='['+id+'] is not an integer'
        elif t == 'float':
            if not match( r'^[0-9]+((\.|\,)[0-9]+)?$', v):
                err='['+id+'] is not a float'
        elif t == 'phone':
            if not match( r'^[\(\)0-9\t\ \-\.\+]{6,26}$', v):
                err='['+id+'] is not a valid phone number'
        elif t == 'checkbox':
            pass
        elif t == 'hidden':
            pass
        elif t == 'string_ro':
            _v = self.fields[id].get('value')
            if _v and (_v != v):
                err='['+id+'] is read only'
        elif t == 'identifier':
            if not match( r'^[a-zA-Z]\w*$', v ):
                err='['+id+'] is not a valid identifier'
        elif t == 'text':
            pass
        elif t == 'selection':
            if type( v ) is type( [] ):
                for vv in v:
                    if vv not in f['mvalue'].keys():
                        err='Invalid multi selection for ['+id+']'
                        break
            elif v not in f['mvalue'].keys():
                err='Invalid selection for ['+id+']'
        elif t == 'radio':
            if v not in f['mvalue'].keys():
                err='Invalid selection for ['+id+']'
        elif t == 'date':
            if not match( r'^[0-9]?[0-9]/[0-9]?[0-9]/[0-9]{4,4}$', v):
                # FIXME: i18n 
                err='['+id+'] invalid date should be like 12/31/1999'
        elif t == 'url':
            if not match( r'^(http://)?([\w\~](\:|\.|\-|\/|\?|\=)?){2,}$', v ):
                err='['+id+'] is not a valid url'
        elif t == 'password':
            pass
        elif t == 'file':
            if not v.filename and f.get('required',0):
                err='['+id+'] is required'
            elif v.filename:
                ml = int(f.get( 'maxlength', '0' ))
                if v.read(1) == "":
                    err = '['+id+'] is an empty file'
                    self.REQUEST.form[id] = v.filename                    
                elif ml:
                    if len( v.read( ml + 1 ) ) == ml + 1:
                        err = '['+id+'] is too big, maximum size is %d' % ml
                        self.REQUEST.form[id]=v.filename                        
                v.seek(0)


        return err

    def _mvalue_to_str( self, m ):
        # convert a mvalue dico into a string
        if type(m) is not type({}) :
            return ''
        str = ''
        keys = m.keys()
        keys.sort()
        for k in keys:
            str = str + k + ' | ' + m[k] + '\n'
        return str

    def _str_to_mvalue( self, s ):
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

    def get_values( self, no_fd=1 ):
        # return dico field:value
        v = {}
        form = self.REQUEST.form
        for f in self.getFList( 1 ):
            if no_fd and self.fields[f]['type'] == 'file':
                v[f] = form.get(f).filename
            else:
                v[f] = form.get(f)
        return v

Globals.InitializeClass(Form)
# EOC Form
