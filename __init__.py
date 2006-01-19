# Copyright (c) 2002-2004 Nuxeo SARL <http://nuxeo.com>
# $Id$

import sys

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.permissions import AddPortalContent

from Products.CPSCore import CPSBase
from Products.CPSCollector import CollectorDocument
from Products.CPSCollector import QuizDocument
from Products.CPSCollector import CollectorItem

from Products.GenericSetup import profile_registry
from Products.GenericSetup import EXTENSION

from Products.CPSCore.interfaces import ICPSSite

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

registerDirectory('skins/cps', globals())

def initialize(registrar):
    utils.ContentInit(
        'CPSCollector',
        content_types = contentClasses,
        permission = AddPortalContent,
        extra_constructors = contentConstructors,
        fti = fti,
        ).initialize(registrar)
    profile_registry.registerProfile(
        'default',
        'CPS Collector',
        "CPSCollector product for CPS.",
        'profiles/default',
        'CPSCollector',
        EXTENSION,
        for_=ICPSSite)
