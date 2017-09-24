# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 S&C (<http://arc.pe>).
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
from openerp import api
from openerp.osv import fields,osv
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class account_invoice(osv.osv):
	_inherit = 'account.invoice'

	def _partner_amount_positive(self, cr, uid, ids, field_name, arg, context=None):
		res = dict(map(lambda x: (x,0), ids))
		try:
			favor = 0.00
			for invoice in self.browse(cr, uid, ids, context):
				debe = sum(invoice_id.amount_total for invoice_id in invoice.partner_id.invoice_ids  if invoice_id.state != 'cancel')
				haber = sum(pago.amount for pago in invoice.partner_id.pagos_ids)
				favor = haber - debe
				res[invoice.id] = favor
		except:
			pass
		return res

	@api.multi
	@api.depends('amount_total', 'pagos_ids')
	def _compute_saldo(self):
		pagos = sum(pago.amount for pago in self.pagos_ids)
		self.saldo = self.amount_total - pagos
		self.pagos_realizados = pagos

	_columns = {
		'partner_amount_positive': fields.function(_partner_amount_positive, string='Monto a favor', digits=dp.get_precision('Account'), type='float'),
		'saldo': fields.float(string='Saldo', digits=dp.get_precision('Account'), compute='_compute_saldo'),
		'pagos_ids': fields.one2many('takana.payment.invoice', 'invoice_id', 'Pagos', copy=True),
		'pagos_realizados': fields.float(string='Pagos realizados', digits=dp.get_precision('Account'), compute='_compute_saldo'),
	}