# $Id$
# Collector collects input from a form

### import
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem


### class
class CollectorItem(SimpleItem):
    "CollectorItem class"
    meta_type = 'CollectorItem'
    manage_options = (
        { 'label':'View', 'action':'view' },
        )+SimpleItem.manage_options 

    def __init__( self, id, form ):
        "construtor"
        self.id = id
        self.data = form
        self._p_changed = 1

    def view( self ):
        "view"
        return str( self.data )

InitializeClass(CollectorItem)
    
### EOF
