## $Id$
doc = context.getContent()

f_id = context.REQUEST.form.get('f_id')
doc.move_fields(f_id, 'down')

if doc.meta_type == 'Quiz Document':
    return context.Form_editQuizForm()
else:
    return context.Form_editForm()
