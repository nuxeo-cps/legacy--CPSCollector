# Copyright (c) 2002-2004 Nuxeo SARL <http://nuxeo.com>
# $Id$
""" 
A collector item encapsulates input from a form 

"""
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent

class CollectorItem(SimpleItem):
    security = ClassSecurityInfo()    

    meta_type = 'CollectorItem'
    manage_options = ( { 'label':'View', 'action':'view' },
                       ) + SimpleItem.manage_options 
    
    def __init__(self, id, form):
        """Construtor"""
        self.id = id
        self.data = form
        self._p_changed = 1
        
    security.declareProtected(ModifyPortalContent, 'view')
    def view(self):
        """View"""
        return str(self.data)

InitializeClass(CollectorItem)
