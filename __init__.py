# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# $Id$

import sys

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import AddPortalContent

from Products.NuxCPSDocuments import BaseDocument
from Products.NuxCPSCollector import CollectorDocument
from Products.NuxCPSCollector import CollectorItem

contentClasses = (CollectorDocument.CollectorDocument,
                  CollectorItem.CollectorItem,
                  )

contentConstructors = (CollectorDocument.addCollectorDocument,
                       )

fti = (CollectorDocument.factory_type_information +
       ())

bases = (BaseDocument.BaseDocument,) # base zclasses

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
