## $Id$

doc = context.getContent()
id = context.REQUEST.form.get('id')
t = context.REQUEST.form.get('type')
doc.add_field(id, type=t)
context.REQUEST.form['f_id']=id

return context.Form_editField()
