## $Id$

doc = context.getContent()
zpt_name = doc.process_edit_field(proxy=context)
zpt = getattr(context, zpt_name)

return zpt()
