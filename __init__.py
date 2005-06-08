# Copyright (c) 2002-2004 Nuxeo SARL <http://nuxeo.com>
# $Id$

import sys

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.permissions import AddPortalContent

from Products.CPSCore import CPSBase
bases = (CPSBase.CPSBaseDocument,) # base zclasses
from Products.CPSCollector import CollectorDocument
from Products.CPSCollector import QuizDocument
from Products.CPSCollector import CollectorItem

contentClasses = (CollectorDocument.CollectorDocument,
                  QuizDocument.QuizDocument,
                  CollectorItem.CollectorItem,
                  )

contentConstructors = (CollectorDocument.addCollectorDocument,
                       QuizDocument.addQuizDocument,
                       )

fti = (CollectorDocument.factory_type_information +
       QuizDocument.factory_type_information +
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
