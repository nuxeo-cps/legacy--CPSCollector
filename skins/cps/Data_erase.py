##parameters=REQUEST

# $Id$

doc = context.getContent()
doc.eraseData()

REQUEST.RESPONSE.redirect(context.absolute_url() +
                          '/?portal_status_message=collector_psm_erased_data')
