# -*- encoding: utf-8 -*-
##############################################################################
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

import time
import netsvc
import c2c_pack_product_chg

from magentoerpconnect import magerp_osv
from tools.translate import _
from osv import osv
from osv import fields

ORDER_STATUS_MAPPING = {'draft': 'processing', 'progress': 'processing', 'shipping_except': 'complete', 'invoice_except': 'complete', 'done': 'closed', 'cancel': 'canceled', 'waiting_date': 'holded'}


class sale_order(magerp_osv.magerp_osv):
    _inherit = "sale.order"
    

    def get_order_cash_on_delivery(self, cr, uid, res, external_referential_id, data_record, key_field, mapping_lines, defaults, context):
        """Get cash on delivery amounts on orders imported from magento"""
        if data_record.get('cod_fee', False) and float(data_record.get('cod_fee', False)) > 0:
            cod_product_id = self.pool.get('product.product').search(cr, uid, [('default_code', '=', 'CASH ON DELIVERY MAGENTO')])[0]
            cod_product = self.pool.get('product.product').browse(cr, uid, cod_product_id, context)

            # simple VAT tax on cash on delivery
            tax_id = []
            if data_record['cod_tax_amount'] and float(data_record['cod_tax_amount']) != 0:
                cod_tax_vat = float(data_record['cod_tax_amount'])/float(data_record['cod_fee'])
                cod_tax_ids = self.pool.get('account.tax').search(cr, uid, [('type_tax_use', '=', 'sale'), ('amount', '>=', cod_tax_vat - 0.001), ('amount', '<=', cod_tax_vat + 0.001)])
                if cod_tax_ids and len(cod_tax_ids) > 0:
                    tax_id = [(6, 0, [cod_tax_ids[0]])]
            res['order_line'].append((0, 0, {
                                        'product_id': cod_product.id,
                                        'name': cod_product.name,
                                        'product_uom': cod_product.uom_id.id,
                                        'product_uom_qty': 1,
                                        'price_unit': float(data_record['cod_fee']),
                                        'tax_id': tax_id
                                    }))
        return res

    def get_order_lines(self, cr, uid, res, external_referential_id, data_record, key_field, mapping_lines, defaults, context):
        """Add cash on delivery on orders imported from magento"""
        res = super(sale_order, self).get_order_lines(cr, uid, res, external_referential_id, data_record, key_field, mapping_lines, defaults, context)
        res = self.get_order_cash_on_delivery(cr, uid, res, external_referential_id, data_record, key_field, mapping_lines, defaults, context)
        return res

    def oe_create(self, cr, uid, vals, data, external_referential_id, defaults, context):
        """call sale_markup's module on_change to compute margin when order's created from magento"""
        order_id = super(sale_order, self).oe_create(cr, uid, vals, data, external_referential_id, defaults, context)
        order_line_obj = self.pool.get('sale.order.line')
        order = self.browse(cr, uid, order_id, context)
        for line in order.order_line:
            # Call line oin_change to record margin
            # line_changes = order_line_obj.onchange_price_unit(cr, uid, line.id, line.price_unit, line.product_id.id, line.discount, line.product_uom.id, order.pricelist_id.id, line.property_ids, override_unit_price = False)
            # # Always keep the price from Magento
            # line_changes['value']['price_unit'] = line.price_unit
            # order_line_obj.write(cr, uid, line.id, line_changes['value'], context=context)

        return order_id

    def action_invoice_create(self, cr, uid, ids, grouped=False, states=['confirmed', 'done', 'exception']):
        """ open invoices directly (bypass draft) when created from an order"""
        invoice_id = super(sale_order, self).action_invoice_create(cr, uid, ids, grouped, states)
        if invoice_id:
            invoice = self.pool.get('account.invoice').browse(cr, uid, invoice_id)
            if invoice.state == 'draft':
                wf_service = netsvc.LocalService("workflow")
                wf_service.trg_validate(uid, 'account.invoice',
                                        invoice_id, 'invoice_open', cr)
        return invoice_id
        
    def _invoice_date_get(self, cr, uid, ids, field_name, arg, context):
        res={}
        for id in ids:
            res[id]=False
        cr.execute("SELECT rel.order_id,MIN(inv.date_invoice) FROM sale_order_invoice_rel rel \
        JOIN account_invoice inv ON (rel.invoice_id=inv.id) WHERE rel.order_id IN %s \
        GROUP BY rel.order_id", (tuple(ids),))
        for line in cr.fetchall():
            res[line[0]] = line[1]
        return res

    def _invoiced_date_search(self, cr, uid, obj, name, args, context):
        if not len(args):
            return []
        new_args = []
        ids=[]
        for argument in args:
            operator = argument[1]
            value = argument[2]
            cr.execute("SELECT rel.order_id FROM sale_order_invoice_rel rel \
            JOIN account_invoice inv ON (rel.invoice_id=inv.id) WHERE inv.date_invoice IS NOT NULL AND \
            inv.date_invoice "+operator+" %s", (str(value),))
            for line in cr.fetchall():
                ids.append(line[0])
        if ids:
            new_args.append( ('id','in',ids) )
        return new_args
                
    _columns = {
        'date_invoiced': fields.function(_invoice_date_get, method=True, fnct_search=_invoiced_date_search,
            type='date', string='Invoice Date', help="Date of the first invoice generated for this SO"),
    }

sale_order()

class sale_shop(magerp_osv.magerp_osv):

    _inherit = 'sale.shop'

    def deactivate_products(self, cr, uid, context=None):
        """
        Deactivate all products planned to deactivation on OpenERP
        Only if no picking uses the product
        """

        product_ids = self.pool.get('product.product').search(cr, uid, [('to_deactivate', '=', True)])
        self.pool.get('product.product').try_deactivate_product(cr, uid, product_ids, context=context)
        return True

    def export_catalog(self, cr, uid, ids, context=None):
        """
            Changes from magentoerpconnect : add the auto deactivation of products at the end of the export
        """

        if context is None:
            context = {}
        for shop in self.browse(cr, uid, ids):
            context['shop_id'] = shop.id
            context['conn_obj'] = self.external_connection(cr, uid, shop.referential_id)
            self.export_categories(cr, uid, shop, context)
            self.export_products(cr, uid, shop, context)
            shop.write({'last_products_export_date': time.strftime('%Y-%m-%d %H:%M:%S')})

        cr.commit()
        self.deactivate_products(cr, uid, context=context)
        self.export_inventory(cr, uid, ids, context)
        return False

    def update_shop_orders(self, cr, uid, order, ext_id, ctx):
        conn = ctx.get('conn_obj', False)
        status = ORDER_STATUS_MAPPING.get(order.state, False)
        result = {}

        #status update:
        if status:
            result['status_change'] = conn.call('sales_order.addComment', [ext_id, status, '', False])
            # If status has changed into OERP and the order need_to_update, then we consider the update is done
            # remove the 'need_to_update': True
            if order.need_to_update:
                self.pool.get('sale.order').write(cr, uid, order.id, {'need_to_update': False})
                cr.commit()

        #creation of Magento invoice eventually:
        # remove invoice creation for debonix
#        cr.execute("select account_invoice.id from account_invoice inner join sale_order_invoice_rel on invoice_id = account_invoice.id where order_id = %s" % order.id)
#        resultset = cr.fetchone()
#        if resultset and len(resultset) == 1:
#            invoice = self.pool.get("account.invoice").browse(cr, uid, resultset[0])
#            if invoice.amount_total == order.amount_total and not invoice.magento_ref:
#                try:
#                    result['magento_invoice_ref'] = conn.call('sales_order_invoice.create', [order.magento_incrementid, [], _("Invoice Created"), True, True])
#                    self.pool.get("account.invoice").write(cr, uid, invoice.id, {'magento_ref': result['magento_invoice_ref'], 'origin': result['magento_invoice_ref']})
#                except Exception, e:
#                    pass #TODO make sure that's because Magento invoice already exists and then re-attach it!

        return result

sale_shop()


c2c_pack_product_chg.sale.sale_order_line.BASE_TEXT_FOR_PRD_REPLACE = _("""This product replaces partially or completely the ordered product :
""")

def invoice_line_create(self, cr, uid, ids, context={}):
    """Override this method to add a create the line with the replaced product in the related packing
    (but same price as original product). Add a comment which indicates the modification

    CHANGE FROM C2C_PACK_PRODUCT_CHG: DELETE NOTE BEFORE UPDATE LINE"""
    inv_created_ids = super(c2c_pack_product_chg.sale.sale_order_line, self).invoice_line_create(cr, uid, ids, context)

    prod_obj = self.pool.get('product.product')
    partner_obj = self.pool.get('res.partner')
    inv_line_obj = self.pool.get('account.invoice.line')

    inv_line_obj.write(cr, uid, inv_created_ids, {'note': ''})
    for so_line in self.browse(cr, uid, ids):
        product_changed_id = False
        # If one of the stock move generated by the SO lines has
        # a product replaced
        for move in so_line.move_ids:
            if move.old_product_id:
                product_changed_id = move.product_id.id
                break
        # we replace the product on the invoice
        # but keep the price of the original product
        if product_changed_id:
            if so_line.invoice_lines:
                # We add a comment into all related invoices lines
                inv_line_ids_to_change = [inv_line.id for inv_line in so_line.invoice_lines]
                lang = partner_obj.browse(cr, uid, so_line.order_id.partner_id.id).lang
                context = {'lang': lang}
                for inv_line in inv_line_obj.browse(cr, uid, inv_line_ids_to_change):
                    note = ''
                    product_note = inv_line.name
                    product_name = prod_obj.name_get(cr, uid, [product_changed_id], context=context)[0][1]
                    result = inv_line_obj.product_id_change(cr, uid,
                                                            inv_line.id,
                                                            product_changed_id,
                                                            inv_line.uos_id.id,
                                                            qty=inv_line.quantity,
                                                            name=product_name,
                                                            type='out_invoice',
                                                            partner_id=so_line.order_id.partner_id.id,
                                                            fposition_id=so_line.order_id.partner_id.property_account_position.id,
                                                            price_unit=inv_line.price_unit,
                                                            context=context)

                    new_note = note + self.BASE_TEXT_FOR_PRD_REPLACE + product_note
                    inv_line_obj.write(cr, uid, inv_line.id, {'note': new_note,
                                                              'account_id': result['value']['account_id'],
                                                              'invoice_line_tax_id': result['value']['invoice_line_tax_id'],
                                                              'uos_id': result['value']['uos_id'],
                                                              'name': product_name,
                                                              'product_id': product_changed_id})
    return inv_created_ids

c2c_pack_product_chg.sale.sale_order_line.invoice_line_create = invoice_line_create
