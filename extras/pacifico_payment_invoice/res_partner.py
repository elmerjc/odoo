# -*- coding: utf-8 -*-

from openerp.osv import fields,osv
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp

class res_partner(osv.osv):
	_inherit = 'res.partner'

	def _amount_positive(self, cr, uid, ids, field_name, arg, context=None):
		res = dict(map(lambda x: (x,0), ids))
		partner = self.browse(cr, uid, ids, context)

		try:
			for partner_id in partner:
				debe = sum(invoice_id.amount_total for invoice_id in partner_id.invoice_ids  if invoice_id.state != 'cancel')
				haber = sum(pago.amount for pago in partner_id.pagos_ids)
			res[partner.id] = haber - debe
		except:
			pass
		return res

	_columns = {
		'amount_positive': fields.function(_amount_positive, string='Monto a favor', digits=dp.get_precision('Account'), type='float'),
		'pagos_ids': fields.one2many('pacifico.payment.invoice', 'partner_id', 'Pagos'),
		'invoice_ids': fields.one2many('account.invoice','partner_id','Facturas'),
	}