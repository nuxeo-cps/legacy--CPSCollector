##parameters=REQUEST

# $Id$
doc = context.getContent()

f_id = REQUEST.form.get('f_id')
doc.del_fields(f_id)

if doc.meta_type == 'Quiz Document':
    return context.Form_editQuizForm()
else:
    return context.Form_editForm()
