# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import fields,osv
import openerp.addons.decimal_precision as dp

class account_invoice(osv.osv):
	_inherit = 'account.invoice'

	def _partner_amount_positive(self, cr, uid, ids, field_name, arg, context=None):
		res = dict(map(lambda x: (x,0), ids))
		try:
			for invoice in self.browse(cr, uid, ids, context):
				debe = sum(invoice_id.amount_total for invoice_id in invoice.partner_id.invoice_ids  if invoice_id.state != 'cancel')
				haber = sum(pago.amount for pago in invoice.partner_id.pagos_ids)
			res[invoice.id] = haber - debe
		except:
			pass
		return res

	@api.multi
	@api.depends('payment_line')
	def _compute_saldo(self):
		pagos = sum(pago.amount for pago in self.payment_line)
		total = sum(line.price_subtotal for line in self.invoice_line)
		self.saldo = total - pagos
		self.pagos_realizados = pagos

	_columns = {
		'partner_amount_positive': fields.function(_partner_amount_positive, string='Monto a favor', digits=dp.get_precision('Account'), type='float'),
		'saldo': fields.float(string='Saldo', digits=dp.get_precision('Account'), compute='_compute_saldo', readonly=True),
		'pagos_realizados': fields.float(string='Pagos realizados', digits=dp.get_precision('Account'), compute='_compute_saldo'),
		'payment_line': fields.one2many('pacifico.payment.invoice', 'invoice_id', 'Pagos'),
	}