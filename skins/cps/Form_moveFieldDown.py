## $Id$
doc = context.getContent()

f_id = context.REQUEST.form.get('f_id')
doc.move_fields(f_id, 'down')
return context.Form_editForm()
