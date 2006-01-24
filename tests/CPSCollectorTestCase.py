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
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.CPSDefault.tests.CPSTestCase import CPSTestCase, MANAGER_ID

# needeed products besides cps default ones
ZopeTestCase.installProduct('CPSCollector')

class CPSCollectorTestCase(CPSTestCase):

    def afterSetUp(self):
        CPSTestCase.afterSetUp(self)
        # XXX AT: it makes no sense to set up local roles globally...
        self.login(MANAGER_ID)
        self.addMember('wsman', 'secret',
                       roles=['Member', 'WorkspaceManager', 'SectionReader'])
        if 'cps_collector_installer' not in self.portal.objectIds():
            installer = ExternalMethod(
                'cps_collector_installer',
                '',
                'CPSCollector.install',
                'install')
            self.portal._setObject('cps_collector_installer',
                                   installer)
        self.portal.cps_collector_installer()

    def addMember(self, uid, passwd, roles=[]):
        mdir = self.portal.portal_directories['members']
        mdir._createEntry({'id' : uid,
                           'sn' : uid,
                           'passwd' : passwd,
                           'roles' : roles,
                           }
                          )
