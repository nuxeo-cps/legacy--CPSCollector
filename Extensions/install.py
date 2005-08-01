# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
# Author: Julien Anguenot <ja@nuxeo.com>
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

"""
CPSCollector Installer

HOWTO USE THAT ?

 - Log into the ZMI as manager
 - Go to your CPS root directory
* - Create an External Method with the following parameters:

     id    : CPSCollector Installer (or whatever)
     title : CPSCollector Installer (or whatever)
     Module Name   :  CPSCollector.install
     Function Name : install

 - save it
 - click now the test tab of this external method.
 - that's it !

"""

from Products.CPSInstaller.CPSInstaller import CPSInstaller

def install(self):
    """
    Starting point !
    """

    ##############################################
    # Create the installer
    ##############################################
    installer = CPSInstaller(self, 'CPSCollector')
    installer.log("Starting CPSCollector Install")

    #################################################
    # PORTAL TYPES
    #################################################
    t = 'typeinfo_name'
    ptypes = {
        'Collector Document': {
            t: 'CPSCollector: Collector Document (Collector Document)',
            'add_meta_type': 'Factory-based Type Information',
            'allowed_content_types': (),
            },
       'Quiz Document': {
            t: 'CPSCollector: Quiz Document (Quiz Document)',
            'add_meta_type': 'Factory-based Type Information',
            'allowed_content_types': (),
            },
    }
    installer.verifyContentTypes(ptypes)
    installer.allowContentTypes(('Collector Document','Quiz Document'),
                                'Workspace')

    ########################################
    #   WORKFLOW ASSOCIATIONS
    ########################################
    ws_chains = { 'Collector Document': 'workspace_content_wf',
                  'Quiz Document': 'workspace_content_wf', }
    se_chains = { 'Collector Document': 'section_content_wf',
                  'Quiz Document': 'section_content_wf', }
    installer.verifyLocalWorkflowChains(installer.portal['workspaces'],
                                        ws_chains)
    installer.verifyLocalWorkflowChains(installer.portal['sections'],
                                        se_chains)

    ##########################################
    # SKINS
    ##########################################
    skins = {'cps_collector': 'Products/CPSCollector/skins/cps'}
    installer.verifySkins(skins)

    ##############################################
    # i18n support
    ##############################################
    installer.verifyMessageCatalog('cpscollector', 'CPSCollector messages')
    installer.setupTranslations(message_catalog='cpscollector')

    ##############################################
    # Finished!
    ##############################################
    installer.finalize()
    installer.log("End of CPSCollector install")
    return installer.logResult()
