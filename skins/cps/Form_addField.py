##parameters=REQUEST

# $Id$

doc = context.getContent()
id = REQUEST.form.get('id')
t = REQUEST.form.get('type')
doc.add_field(id, type=t)
REQUEST.form['f_id']=id

return context.Form_editField()
