# $Id$
# Collector collects input from a form

### import
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent

### class
class CollectorItem(SimpleItem):
    security = ClassSecurityInfo()    

    meta_type = 'CollectorItem'
    manage_options = (
        { 'label':'View', 'action':'view' },
        )+SimpleItem.manage_options 

    def __init__( self, id, form ):
        "construtor"
        self.id = id
        self.data = form
        self._p_changed = 1
        
    security.declareProtected(ModifyPortalContent, 'view')
    def view( self ):
        "view"
        return str( self.data )

InitializeClass(CollectorItem)
    
### EOF
