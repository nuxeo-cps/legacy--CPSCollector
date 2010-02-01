# (C) Copyright 2008 Association Paris-Montagne
# Author: Georges Racinet <georges@racinet.fr>
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
# $Id: __init__.py 890 2008-06-18 18:26:32Z joe $

from Products.CMFCore.permissions import setDefaultRoles

ViewCollectorData = 'View collector data'
setDefaultRoles(ViewCollectorData, ('Manager', 'Owner'))

ManageCollectorData = 'Manage collector data'
setDefaultRoles(ManageCollectorData, ('Manager', 'Owner'))
