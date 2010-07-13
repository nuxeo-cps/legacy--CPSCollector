# (C) Copyright 2010 Georges Racinet
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
# $Id$

import logging
import transaction
from Products.CPSUtil.text import upgrade_string_unicode

def upgrade_data_unicode(portal):
    """Upgrade all form data to unicode.
    The form documents themselves should have been treated by
    CPSDocument's step."""

    logger = logging.getLogger(
        'Products.CPSCollector.upgrade.upgrade_data_unicode')
    repotool = portal.portal_repository
    total = len(repotool)

    done = 0
    for doc in repotool.objectValues(['Collector Document']):
        if not _upgrade_form_data_unicode(doc):
            logger.error("Could not upgrade form data for rev %s", doc)
            continue
        done += 1
        logger.info("Upgraded data for %d/%d form documents", done, total)
        transaction.commit()

    logger.warn("Finished upgrade of data to unicode for %d/%d form documents",
                done, total)
    logger.warn("Finished unicode upgrade of the %d/%d documents.", done, total)
    transaction.commit()

def _upgrade_form_data_unicode(doc):
    fields = doc.fields
    new_fields = {}
    for fid, descr in fields.items():
        new_fields[upgrade_string_unicode(fid)] = dict(
            (k, upgrade_string_unicode(v)) for k, v in descr.items())
    doc.fields = new_fields

    doc.fields_list = [upgrade_string_unicode(fid) for fid in doc.fields_list]
    doc._p_changed = 1

    for item in doc.objectValues(['CollectorItem',]):
        item.data = dict((upgrade_string_unicode(k), upgrade_string_unicode(v))
                         for k,v in item.data.items())
        item._p_changed = 1
    return True
