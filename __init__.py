# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# $Id$

import sys

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import AddPortalContent

try:
    # CPS3
    from Products.NuxCPS3 import CPSBase
    bases = (CPSBase.CPSBaseDocument,) # base zclasses

except ImportError:
    # CPS2
    from Products.NuxCPSDocuments import BaseDocument
    bases = (BaseDocument.BaseDocument,) # base zclasses
    
from Products.NuxCPSCollector import CollectorDocument
from Products.NuxCPSCollector import CollectorItem

contentClasses = (CollectorDocument.CollectorDocument,
                  CollectorItem.CollectorItem,
                  )

contentConstructors = (CollectorDocument.addCollectorDocument,
                       )

fti = (CollectorDocument.factory_type_information +
       ())


this_module = sys.modules[__name__]
z_bases = utils.initializeBasesPhase1(bases, this_module)

registerDirectory('skins/cps2', globals())
registerDirectory('skins/cps3', globals())

def initialize(registrar):
    utils.initializeBasesPhase2(z_bases, registrar)
    utils.ContentInit(
        'NuxCPSCollector',
        content_types = contentClasses,
        permission = AddPortalContent,
        extra_constructors = contentConstructors,
        fti = fti,
        ).initialize(registrar)
# EOF