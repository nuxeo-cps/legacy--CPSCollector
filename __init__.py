# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# $Id$

import sys

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import AddPortalContent

from Products.CPSCore import CPSBase
bases = (CPSBase.CPSBaseDocument,) # base zclasses
from Products.CPSCollector import CollectorDocument
from Products.CPSCollector import CollectorItem

contentClasses = (CollectorDocument.CollectorDocument,
                  CollectorItem.CollectorItem,
                  )

contentConstructors = (CollectorDocument.addCollectorDocument,
                       )

fti = (CollectorDocument.factory_type_information +
       ())


this_module = sys.modules[__name__]
z_bases = utils.initializeBasesPhase1(bases, this_module)

registerDirectory('skins/cps', globals())

def initialize(registrar):
    utils.initializeBasesPhase2(z_bases, registrar)
    utils.ContentInit(
        'CPSCollector',
        content_types = contentClasses,
        permission = AddPortalContent,
        extra_constructors = contentConstructors,
        fti = fti,
        ).initialize(registrar)

# EOF
