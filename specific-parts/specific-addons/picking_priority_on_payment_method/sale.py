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

from openerp.osv import orm, fields


class sale_order(orm.Model):
    _inherit = 'sale.order'

    def __selection_priority(self, cr, uid, context=None):
        picking_obj = self.pool['stock.picking']
        return picking_obj.get_selection_priority(cr, uid, context=context)

    _columns = {
        'picking_priority': fields.selection(
            __selection_priority,
            'Delivery Orders Priority',
            help='The priority of the picking'),
    }

    def onchange_payment_method_id(self, cr, uid, ids, payment_method_id,
                                   context=None):
        result = super(sale_order, self).onchange_payment_method_id(
            cr, uid, ids, payment_method_id, context=context)
        if payment_method_id:
            method_obj = self.pool.get('payment.method')
            method = method_obj.browse(cr, uid, payment_method_id,
                                       context=context)
            if method.picking_priority:
                result.setdefault('value', {})
                result['value']['picking_priority'] = method.picking_priority
        return result

    def _prepare_order_picking(self, cr, uid, order, context=None):
        """ set stock picking priority """
        res = super(sale_order, self)._prepare_order_picking(
            cr, uid, order, context=context)
        if order.picking_priority:
            res['priority'] = order.picking_priority
        return res
