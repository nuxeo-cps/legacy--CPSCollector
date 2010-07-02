##parameters=REQUEST

ob=context.getContent()
ob.mergeRevisionsData(proxy=context)

REQUEST.RESPONSE.redirect(
    context.absolute_url() + '?portal_status_message=collector_merged_data')

