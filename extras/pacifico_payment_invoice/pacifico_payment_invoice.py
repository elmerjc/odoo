# -*- coding: utf-8 -*-

from openerp import api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.osv import fields, osv, expression
import openerp.addons.decimal_precision as dp

class pacifico_payment_invoice(osv.osv):
	_name = 'pacifico.payment.invoice'
	_description = 'Pagos de las facturas del cliente'
	_order = 'date'

	_columns = {
		'name': fields.char('Operación'),
		'sequence': fields.integer('Secuencia', default=1),
		'invoice_id': fields.many2one('account.invoice', 'Factura', ondelete='cascade'),
		'date': fields.date('Fecha', required=True),
		'metodo': fields.selection([('Continental', 'Continental'),('Interbank', 'Interbank'),('BCP', 'BCP'),('Efectivo', 'Efectivo')], 'Metodo'),
		'amount': fields.float('Monto', digits=dp.get_precision('Account'), store=True, required=True, change_default=True),
		'state': fields.selection([('open', 'Abierto'), ('close', 'Cerrado')], 'Estado', default='open'),
		'invoice_total': fields.float('Total', related='invoice_id.amount_total', readonly=True),
		'invoice_name': fields.char('Pedido', related='invoice_id.name', readonly=True, store=True),
		'invoice_number': fields.char('Numero', related='invoice_id.number', readonly=True, store=True),
		'partner_id': fields.related('invoice_id', 'partner_id', type='many2one', relation='res.partner', string='Cliente', readonly=True, store=True),
		'comment': fields.text('Observaciones', store=True, readonly=True, copy=False),
	}

	_defaults = {
		'date': fields.datetime.now,
	}

	def check_pago_change(self, cr, uid, ids, invoice, partner_id, monto, total, context=None):

		invoice_obj = self.pool.get('account.invoice')
		invoice_id = invoice_obj.search(cr, uid, [('number', '=', invoice)], context=context)
		invoice_data = invoice_obj.browse(cr, uid, invoice_id, context=context)

		if invoice_data.state == 'open':
			pago_ids = self.search(cr, uid, [('invoice_id', '=', invoice_id)], context=context)
			pagos = self.browse (cr, uid, pago_ids, context=context)
			partner_obj = self.pool.get('res.partner')
			partner_data = partner_obj.browse(cr, uid, partner_id, context=context)

			debe = total
			haber = sum(pago.amount for pago in pagos)
			amortizacion = monto
			saldo = debe - haber

			val = {
				'amount' : monto
			}

			if saldo > 0:
				if amortizacion > saldo:
					#raise Warning(_('Pago a favor'), _("Se agrego al cliente %s un monto a favor") % (partner_data.name) )
					invoice_obj.write(cr, uid, invoice_id, {'state': 'paid'})
					self.write(cr, uid, ids, {'state': 'close'})
					return {'value' : val}
				else:
					if amortizacion == saldo:
						invoice_obj.write(cr, uid, invoice_id, {'state': 'paid'})
						self.write(cr, uid, ids, {'state': 'close'})
						return {'value' : val}
					else:
						invoice_obj.write(cr, uid, invoice_id, {'state': 'open'})
						return {'value' : val}
			else:
				raise except_orm(_('Error en el pago'), _("La factura ya fue pagada") )
				return {'value' : val}
		else:
			raise except_orm(_('Error de estado'), _("No se puede ingresar pagos en esta factura") )