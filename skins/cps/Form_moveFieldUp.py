## $Id$
doc = context.getContent()

f_id = context.REQUEST.form.get('f_id')
doc.move_fields(f_id, 'up')
return context.Form_editForm()
