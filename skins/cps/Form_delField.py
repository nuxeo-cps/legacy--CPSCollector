##parameters=REQUEST

# $Id$

f_id = REQUEST.form.get('f_id')
doc = context.getEditableContent() # del_fields will always change the doc
doc.del_fields(f_id)

if doc.meta_type == 'Quiz Document':
    return context.Form_editQuizForm()
else:
    return context.Form_editForm()
