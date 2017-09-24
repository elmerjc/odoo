# -*- encoding: utf-8 -*-

from openerp.report import report_sxw
from openerp.osv import osv

class report_sale_order_wizard(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        if context is None:
            context = {}
        super(report_sale_order_wizard,self).__init__(cr,uid,name, context=context)
        self.localcontext.update({
            'get_data_sale_order':self._get_data_sale_order,
            })
        self.context = context

    def _get_data_sale_order(self):
        wizard_obj=self.pool.get('wizard.report.sale.order')
        wizard_data=wizard_obj.browse(self.cr,self.uid,self.ids)

        where_partner_id = ""

        if wizard_data.partner_id.id:
            where_partner_id = " AND rp.id = %s " % (wizard_data.partner_id.id)

        query = """
             SELECT
              so.name AS numero,
              TO_CHAR(so.date_order, 'YYYY-MM-DD') AS date_order,
              so.partner_id,
              rp.name AS cliente,
              so.user_id,
              rp2.name AS responsable,
              so.residual,
              so.amount_total
            FROM sale_order so
            INNER JOIN res_partner rp ON so.partner_id = rp.id
            INNER JOIN res_users ru ON so.user_id = ru.id
            INNER JOIN res_partner rp2 ON ru.partner_id = rp2.id
            WHERE so.date_order >= '%s' AND so.date_order <= '%s' %s 
            ORDER BY so.date_order
        """ % (wizard_data.date_inicio, wizard_data.date_fin, where_partner_id)

        self.cr.execute(query)
        _res = self.cr.dictfetchall()
        return _res

class report_sale_order(osv.AbstractModel):
    _name="report.bolivia_report.report_sale_order"
    _inherit="report.abstract_report"
    _template="bolivia_report.report_sale_order"
    _wrapped_report_class=report_sale_order_wizard
    
    
