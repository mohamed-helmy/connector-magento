# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author Guewen Baconnier. Copyright Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
from base_external_referentials import external_osv
from magentoerpconnect import magerp_osv
import netsvc
from tools.translate import _
import time


class sale_shop(external_osv.external_osv):
    _inherit = "sale.shop"

    def export_inventory(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for shop in self.browse(cr, uid, ids):

            context['shop_id'] = shop.id
            context['conn_obj'] = self.external_connection(cr, uid, shop.referential_id)
            product_ids = [product.id for product in shop.exportable_product_ids]
            if shop.last_inventory_export_date:
                recent_move_ids = self.pool.get('stock.move').search(cr, uid, [
                        ('date_planned', '>', shop.last_inventory_export_date), ('product_id', 'in', product_ids),
                        ('state', '!=', 'draft'), ('state', '!=', 'cancel')])
            else:
                recent_move_ids = self.pool.get('stock.move').search(cr, uid, [('product_id', 'in', product_ids)])
            product_ids = [move.product_id.id for move in self.pool.get('stock.move').browse(cr, uid, recent_move_ids)
                           if move.product_id.state != 'obsolete']
            product_ids = [x for x in set(product_ids)]
            res = self.pool.get('product.product').export_inventory(cr, uid, product_ids, '', context)
            shop.write({'last_inventory_export_date': time.strftime('%Y-%m-%d %H:%M:%S')})

            request = self.pool.get('res.request')
            summary = """%d product stock have been correctly exported.
%d products stock in exception, you should set their stock manually
----------------------------------------------------------------------------------------------""" % (
            res['exported_count'], len(res['exception_products']))
            for product in self.pool.get('product.product').browse(cr, uid, res['exception_products'].keys()):
                summary += """
Product code : %s
Product name %s
Exception :
%s
----------------------------------------------------------------------------------------------""" % (
                product.default_code, product.name, res['exception_products'][product.id])
            request.create(cr, uid,
                           {'name': "Export inventory report",
                            'act_from': uid,
                            'act_to': uid,
                            'body': summary,
                            })

        return True

    def export_shipping(self, cr, uid, ids, context):
        """Export shipping in their order from first to last. Based on the backorder id.
        Only the SQL query is modified on that function"""
        logger = netsvc.Logger()
        for shop in self.browse(cr, uid, ids):
            context['conn_obj'] = self.external_connection(cr, uid, shop.referential_id)

            cr.execute("""
                select stock_picking.id, sale_order.id, count(pickings.id), stock_picking.backorder_id, delivery_carrier.magento_export_needs_tracking, stock_picking.carrier_tracking_ref
                  from stock_picking
                  left join sale_order on sale_order.id = stock_picking.sale_id
                  left join stock_picking as pickings on sale_order.id = pickings.sale_id
                  left join ir_model_data on stock_picking.id = ir_model_data.res_id and ir_model_data.model='stock.picking'
                  left join delivery_carrier on delivery_carrier.id = stock_picking.carrier_id
                 where shop_id = %s and ir_model_data.res_id ISNULL and stock_picking.state = 'done'
                 Group By stock_picking.id, sale_order.id, stock_picking.backorder_id, delivery_carrier.magento_export_needs_tracking, stock_picking.carrier_tracking_ref
                 order by sale_order.id asc, COALESCE(stock_picking.backorder_id, NULL, 0) asc;
                """, (shop.id,))
            results = cr.fetchall()

            success_counter = 0
            exception_pickings = {}
            for result in results:
                if result[2] == 1:
                    picking_type = 'complete'
                else:
                    picking_type = 'partial'

                # only create shipping if a tracking number exists if the flag magento_export_needs_tracking is flagged on the delivery carrier
                if not result[4] or result[5]:
                    ext_shipping_id = False
                    try:
                        ext_shipping_id = self.pool.get('stock.picking').create_ext_shipping(cr, uid, result[0],
                                                                                             picking_type,
                                                                                             shop.referential_id.id,
                                                                                             context)
                    except Exception, e:
                        exception_pickings[result[0]] = e

                    if ext_shipping_id:
                        ir_model_data_vals = {
                            'name': "stock_picking/" + str(ext_shipping_id),
                            'model': "stock.picking",
                            'res_id': result[0],
                            'external_referential_id': shop.referential_id.id,
                            'module': 'extref/' + shop.referential_id.name,
                            }
                        self.pool.get('ir.model.data').create(cr, uid, ir_model_data_vals)
                        cr.commit()
                        logger.notifyChannel('ext synchro', netsvc.LOG_INFO,
                                             "Successfully creating shipping with OpenERP id %s and ext id %s in external sale system" % (
                                             result[0], ext_shipping_id))
                        success_counter += 1

            request = self.pool.get('res.request')
            summary = """Export ended at %s
%d pickings have been correctly exported.
%d pickings in exception
----------------------------------------------------------------------------------------------""" % (
            time.strftime('%Y-%m-%d %H:%M:%S'), success_counter, len(exception_pickings))
            for picking in self.pool.get('stock.picking').browse(cr, uid, exception_pickings.keys()):
                summary += """
Picking reference : %s
Picking origin : %s
Exception :
%s
----------------------------------------------------------------------------------------------""" % (
                picking.name, picking.origin, exception_pickings[picking.id])
            request.create(cr, uid,
                           {'name': "Export pickings report for shop : %s" % shop.name,
                            'act_from': uid,
                            'act_to': uid,
                            'body': summary,
                            })
        return True

    def update_shop_orders(self, cr, uid, order, ext_id, ctx):
        try:
            res = super(sale_shop, self).update_shop_orders(cr, uid, order, ext_id, ctx)
        except Exception, e:
            request = self.pool.get('res.request')
            summary = """Error during orders update on order id : %d
Order reference : %s
Exception :
%s""" % (order.id, order.name, e)
            request.create(cr, uid,
                           {'name': "Update orders error",
                            'act_from': uid,
                            'act_to': uid,
                            'body': summary,
                            })
            cr.commit()
            raise e
        return res

sale_shop()


class sale_order(magerp_osv.magerp_osv):
    _inherit = "sale.order"

    def mage_import_one_by_one(self, cr, uid, conn, external_referential_id, mapping_id, data, defaults=None, context=None):
        if context is None:
            context = {}
        result = {'create_ids': [], 'write_ids': []}
        del(context['one_by_one'])
        for record in data:
            id = record[self.pool.get('external.mapping').read(cr, uid, mapping_id, ['external_key_name'])['external_key_name']]
            get_method = self.pool.get('external.mapping').read(cr, uid, mapping_id, ['external_get_method']).get('external_get_method', False)
            try:
                rec_data = [conn.call(get_method, [id])]
                rec_result = self.ext_import(cr, uid, rec_data, external_referential_id, defaults, context)
                result['create_ids'].append(rec_result['create_ids'])
                result['write_ids'].append(rec_result['write_ids'])
            except Exception, e:
                request = self.pool.get('res.request')
                summary = _("Error during orders import on Magento order id : %s\n\n"
                            "Exception :\n"
                            "%s") % (id, e)
                request.create(cr, uid,
                               {'name': "Import orders error",
                                'act_from': uid,
                                'act_to': uid,
                                'body': summary,
                                })
                raise
        return result

sale_order()
