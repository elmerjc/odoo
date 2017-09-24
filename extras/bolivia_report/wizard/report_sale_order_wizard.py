import datetime
from openerp import tools, api
from openerp.osv import osv, orm, fields
from openerp.tools.translate import _

class report_sale_order_wizard(osv.osv_memory):
    _name = 'wizard.report.sale.order'
    _description = 'Reporte avanzado de pedidos'
    _columns = {
        'date_inicio': fields.date('Desde', required=True),
        'date_fin': fields.date('Hasta', required=True),
        'partner_id': fields.many2one('res.partner', 'Cliente'),
    }

    _defaults = {
        'date_inicio': False,
        'date_fin': False,
    }

    def print_report_sale_order(self,cr,uid,ids,context=None):
        report_data = self.browse(cr,uid,ids,context)
        if report_data.date_inicio > report_data.date_fin:
            raise orm.except_orm(_('Error!'),_('La fecha inicio %s no puede ser mayor a la fecha fin %s') % (report_data.date_inicio,report_data.date_fin))
        data = {
            'date_inicio':report_data.date_inicio,
            'date_fin': report_data.date_fin,
            'partner_id': report_data.partner_id.id,
            }
        return self.pool['report'].get_action(cr,uid,[],'bolivia_report.report_sale_order',data=data,context=context)