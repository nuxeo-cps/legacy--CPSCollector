##parameters=REQUEST

# $Id$

id = REQUEST.form.get('id')
t = REQUEST.form.get('type')
doc = context.getEditableContent() # add_field always change the object
doc.add_field(id, type=t)
REQUEST.form['f_id']=id

return context.Form_editField()
