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


class product_brand(orm.Model):
    _inherit = 'product.brand'

    _columns = {
        'name': fields.char('Name', required=True),
        'product_ids': fields.one2many(
            'product.template', 'brand_id',
            string='Brand',
            ondelete='restrict'),
    }


class product_template(orm.Model):
    _inherit = 'product.template'

    _columns = {
        'brand_id': fields.many2one{
            'product.brand',
            string='Brand',
            ondelete='restrict'),
    }
