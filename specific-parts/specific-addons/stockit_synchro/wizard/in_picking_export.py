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

import base64
import os
import tempfile
from osv import osv, fields
from tools.translate import _
from stockit_synchro.stockit_exporter.exporter import StockitExporter


class StockItInPickingExport(osv.osv_memory):
    _name = 'stockit.export.in.picking'
    _description = 'Export incoming pickings in Stock iT format'

    _columns = {
        'data': fields.binary('File', readonly=True),
    }

    def action_manual_export(self, cr, uid, ids, context=None):
        rows = self.get_data(cr, uid, ids, context)
        exporter = StockitExporter()
        data = exporter.get_csv_data(rows)
        result = self.write(cr,
                            uid,
                            ids,
                            {'data': base64.encodestring(data)},
                            context=context)
        return result

    def action_background_export(self, cr, uid, ids, context=None):
        # TODO: set a filename: manual / generated filename ?
        filename = os.path.join(tempfile.gettempdir(),
                                'in_picking_export.csv')
        rows = self.get_data(cr, uid, ids, context)
        exporter = StockitExporter(filename)
        data = exporter.get_csv_data(rows)
        exporter.export_file(data)

    def get_data(self, cr, uid, ids, context=None):
        """Export incoming pickings in Stock iT format"""
        picking_obj = self.pool.get('stock.picking')
        context['lang'] = 'fr_FR'

        rows = []
        # FIXME: check domain
        picking_ids = picking_obj.search(cr, uid,
                                         [('type', '=', 'in'),
                                          ('state', '=', 'assigned')],
                                         context=context)
        for picking in picking_obj.browse(cr, uid, picking_ids):
            for line in picking.move_lines:
                row = [
                    'E',  # type
                    str(picking.id),  # unique id
                    picking.name,  # ref/name
                    line.date_planned,  # expected date
                    line.product_id.default_code,  # product code
                    line.product_id.x_magerp_zdbx_default_marque and
                    line.product_id.x_magerp_zdbx_default_marque.label or
                    '',  # product brand
                    str(line.product_qty),  # quantity
                    '',  # 6 empty fields for the return of stock it
                    '',
                    '',
                    '',
                    '',
                    '',
                ]
                rows.append(row)

        return rows

StockItInPickingExport()
