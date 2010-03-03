##parameters=REQUEST

# $Id$
form = REQUEST.form
f_id = form.get('id')
t = form.get('type')
doc = context.getEditableContent() # add_field always change the object
doc.add_field(f_id, type=t, insert_after=form.get('insert_after'))
REQUEST.form['f_id']=f_id

return context.Form_editField()
