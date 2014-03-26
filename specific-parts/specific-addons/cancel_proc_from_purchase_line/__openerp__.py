# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2012 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name' : 'Cancel procurement on purchase line unlink',
    'version' : '1',
    'depends' : [
        'procurement',
        'purchase',
     ],
    'author' : 'Camptocamp',
    'description': """
    Removing a purchase order line does not cancel procurements.

    When installed, this module store the origin procurement which
    have generated a purchase order line.
    When a purchase order line is deleted, the procurement
    which had generated it is canceled.

    When purchase orders are merged, if 2 lines have the same
    product but have been generated by 2 different procurements,
    then the 2 lines will be kept distinct in the purchase order.

    Link to a discussion on the subject:
    https://bugs.launchpad.net/openobject-addons/+bug/725860
    """,
    'website': 'http://www.camptocamp.com',
    'data': ['purchase_view.xml',
             ],
    'installable': True,
    'auto_install': False,
}
