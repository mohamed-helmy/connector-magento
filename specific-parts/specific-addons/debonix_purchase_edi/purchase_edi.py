# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Charbel Jacquin (Camptocamp)
#    Copyright 2010-2014 Camptocamp SA
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
from openerp.osv import osv, fields
from openerp.exceptions import Warning

import os
import logging

_logger = logging.getLogger('EDIFACT')

_logger.debug('loading module !')

_spec = None

# class res_company(osv.Model):
#     # TODO, configurable drop dir
#     pass

class purchase_order(osv.Model):
    _inherit = "purchase.order"

    _columns = {
        'create_date': fields.datetime('Creation Time', readonly=True),
        'edifact_sent': fields.boolean('EDI Sent', readonly=True),
        'edifact_removed':  fields.boolean('EDI Removed', readonly=True)
    }

    def generate_edifact(self, cr, uid, ids, context=None):
        import tools.edifact

        # pdb.set_trace()
        mapping = {}
        orders = self.browse(cr, uid, ids, context=context)

        assert len(ids) == 1   # FIXME For now one, we will do batch later

        for order in orders:
            _logger.debug('ORDER: %s' % order.name)

        if order.edifact_sent:
            raise Warning('EDIFACT document already sent to partner, please ask your DBA to clear clear the edifact_sent status on %s if you want to regenerate' % order.name)

        mapping['codefiliale'] = 'PLN'
        mapping['siretFiliale'] = '52789590800012'
        mapping['dateCmd'] = order.date_order.replace('-', '')
        heureCmd = order.create_date.split()[1].replace(':', '')
        mapping['heureCmd'] = heureCmd
        # mapping['heureCmd'] = '090420'

        mapping['codeAgence'] = '928'
        mapping['siretAgence'] = '52789590800012'
        mapping['siretDebonix'] = '49039922700035'

        mapping['noCmd'] = order.name
        mapping['refCmd'] = order.name
        mapping['dateLiv'] = order.minimum_planned_date.replace('-', '')
        mapping['compteDebonix'] = '0000175000'

        mapping['adr1'] = order.dest_address_id.name
        mapping['adr2'] = ''
        mapping['adr3'] = order.dest_address_id.street
        mapping['adr4'] = ''
        mapping['adr5'] = ''
        mapping['cp'] = order.dest_address_id.zip
        mapping['ville'] = order.dest_address_id.city
        mapping['tel'] = order.dest_address_id.phone

        fax = order.dest_address_id.fax
        if fax:
            mapping['fax'] = fax
        else:
            mapping['fax'] = ''
        # add160 Paramètres : commentaire
        # if($donnees->notes) $cmd->add160(utf8_decode($donnees->notes));
        if order.notes:
            mapping['commentaire'] = order.notes
        else:
            mapping['commentaire'] = ''

        order_lines = list(order.order_line)

        lines = []

        def convert_unit(name):
            if name == 'PCE':
                return 'P'
            assert 0 == 1

        totalQty = 0
        totalHT = 0
        for line_index, order_line in enumerate(order_lines):
            line = {}
            line['codag'] = order_line.product_id.code
            line['libelle'] = order_line.product_id.name[:70]

            price_unit = order_line.price_unit
            line['prixUnitaireNet'] = pu = int(price_unit * 10000)

            # call for behave
            # La quantité doit tenir compte du conditionnement remonté dans
            # le champ Quantity du catalogue.
            #
            # Si un client saisie 10 en quantité
            #  sur le site et que le conditionnement présent dans le
            #  champs quantity = 200,  la quantité sera égal  2000 * 1000'
            line['qte'] = int(order_line.product_qty * 1000)

            line['refarticleFournisseur'] = order_line.product_id.code
            line['ligne'] = line_index+1

            montant = int(order_line.price_subtotal * 1000)
            line['montantLigne'] = montant

            totalHT += (pu * montant)
            totalQty += line['qte']

            line['uq'] = convert_unit(order_line.product_uom.name)
            line['dateLiv'] = order_line.date_planned.replace('-', '')
            line['uep'] = 1    # CHECKME

            lines.append(line)

        # 300
        mapping['totalQte'] = totalQty
        mapping['totalLigne'] = line_index+1
        mapping['totalHT'] = int(order.amount_untaxed * 1000)
        mapping['totalTVA'] = int(order.amount_tax * 1000)
        mapping['totalTTC'] = int(order.amount_total * 1000)

        mapping['__lines__'] = lines
        #    for order in po.browse(po_ids):
        #        print order.name
        #        for ol in order.order_line:
        #            print ol
        #        return order
        _logger.debug('DATA extracted [%d] lines', len(lines))
        # assert len(lines) == 1

        doc = tools.edifact.Debonix()
        message = doc.render(mapping)

        _logger.debug('message for %r:\n%r' % (order.name,  message))
        _logger.debug('TODO: Drop it to FTP')
        droppath = '/tmp/edifact'
        filename = '%s.edi' % order.name
        fullpath = os.path.join(droppath, filename)
        os.path.exists(droppath) or os.mkdir(droppath)
        if os.path.exists(fullpath):
            raise Warning("""EDIFACT file %s already present in '%s'.
            Please remove it before you can regenerate""" %
                          (filename,  droppath))
        with open(fullpath, 'w') as out:
            out.write(message.encode('latin1'))

        # order.edifact_sent = True
        res = {'edifact_sent': True}
        self.write(cr, uid, [order.id], res)
        return res
