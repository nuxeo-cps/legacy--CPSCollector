## $Id$

doc = context.getContent()
zpt_name = doc.process_view()
zpt = getattr(context, zpt_name)
return zpt()
