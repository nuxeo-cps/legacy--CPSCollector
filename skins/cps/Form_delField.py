## $Id$
doc = context.getContent()

f_id = context.REQUEST.form.get('f_id')
doc.del_fields(f_id)
return context.Form_editForm()
