##parameters=REQUEST

# $Id$

doc = context.getEditableContent()

doc.eraseData()

if REQUEST is not None: 
    REQUEST.RESPONSE.redirect(context.absolute_url() +
                          '/?portal_status_message=collector_psm_erased_data')
