#!/usr/bin/python
# -*- encoding: iso-8859-15 -*-
# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
# Author: Tarek Ziadé <tz@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
from Testing import ZopeTestCase
from Globals import InitializeClass
from ExtensionClass import Base
from AccessControl import ClassSecurityInfo
from AccessControl.SecurityManagement import newSecurityManager

from Products.CPSDefault.tests import CPSTestCase

class CPSCollectorTestCase(CPSTestCase.CPSTestCase):

    def CpsLogin(self, uid):
        uf = self.portal.acl_users
        user = uf.getUserById(uid).__of__(uf)        
        newSecurityManager(None, user)


class CPSCollectorInstaller(CPSTestCase.CPSInstaller):

    def addMember(self, uid, passwd, roles=[]):
        mdir = self.portal.portal_directories['members']
        mdir._createEntry({'id' : uid,
                           'sn' : uid,
                           'passwd' : passwd,
                           'roles' : roles,
                           }
                          )

    def install(self, portal_id):
        self.addUser()
        self.login()
        self.addPortal(portal_id)
        self.portal = getattr(self.app, portal_id)
        self.fixupTranslationServices(portal_id)
        self.addMember('wsman', 'secret', roles=['Member', 'WorkspaceManager', 'SectionReader'])
        self.logout()

""" setting up a portal for tests

"""
def setupPortal(PortalInstaller=CPSCollectorInstaller):
    app = ZopeTestCase.app()

    if hasattr(app, 'portal'):
        app.manage_delObjects(['portal'])
    CPSCollectorInstaller(app).install('portal')
    ZopeTestCase.close(app)


# needeed products besides cps default ones
ZopeTestCase.installProduct('CPSCollector')

# sets up the portal
setupPortal()
