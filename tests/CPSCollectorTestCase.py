# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
# Authors: Tarek Ziadé <tz@nuxeo.com>
#          Dragos Ivan <div@nuxeo.com>
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
# $Id$

from Products.CPSDefault.tests.CPSTestCase import CPSTestCase
from Products.CPSDefault.tests.CPSTestCase import ExtensionProfileLayerClass
from Products.CPSDefault.tests.CPSTestCase import MANAGER_ID

class LayerClass(ExtensionProfileLayerClass):
    extension_ids = ('CPSCollector:default',)

CPSCollectorLayer = LayerClass(__name__, 'CPSCollectorLayer')


class CPSCollectorTestCase(CPSTestCase):
    layer = CPSCollectorLayer

    def afterSetUp(self):
        CPSTestCase.afterSetUp(self)
        # XXX AT: it makes no sense to set up local roles globally...
        self.login(MANAGER_ID)
        self.addMember('wsman', 'secret',
                       roles=['Member', 'WorkspaceManager', 'SectionReader'])

    def addMember(self, uid, passwd, roles=[]):
        mdir = self.portal.portal_directories['members']
        mdir._createEntry({'id' : uid,
                           'sn' : uid,
                           'passwd' : passwd,
                           'roles' : roles,
                           }
                          )
