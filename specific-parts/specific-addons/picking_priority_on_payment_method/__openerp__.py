# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2014 Camptocamp SA
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

{'name': 'Picking Priority on Payment Method',
 'version': '1.0',
 'author': 'Camptocamp',
 'maintainer': 'Camptocamp',
 'license': 'AGPL-3',
 'category': 'Stock',
 'depends': ['stock_picking_priority',  # stock-logistic-flows
             'sale_payment_method',  # e-commerce-addons
             ],
 'description': """

THIS MODULE IS NO LONGER USED. IT IS STILL THERE SO IT COULD BE UNINSTALLED PROPERLY


Picking Priority on Payment Method
==================================

Add a priority on each payment methods.
Delivery orders are created with the priority of the payment method
used on the origin sales order.
 """,
 'website': 'http://www.camptocamp.com',
 'data': ['sale_view.xml',
          'payment_method_view.xml',
          ],
 'test': [],
 'installable': True,
 'auto_install': False,
}