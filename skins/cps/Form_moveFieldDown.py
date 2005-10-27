##parameters=REQUEST

# $Id$

f_id = REQUEST.form.get('f_id')
doc = context.getEditableContent() # move_fields always changes the doc
doc.move_fields(f_id, 'down')

if doc.meta_type == 'Quiz Document':
    return context.Form_editQuizForm()
else:
    return context.Form_editForm()
