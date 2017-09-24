# -*- coding: utf-8 -*-
{
    'name': "Bolivia Report",
    'summary': """
    	Reporte de bolivia
    """,
    'description': """
        Reporte de bolivia
    """,
    'author': "ARC",
    'website': "http://www.arc.pe",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/report_sale_order_wizard_view.xml',
        'views/bolivia_report_layout.xml',
        'views/report_sale_order.xml',
        'bolivia_report.xml',
    ],
    'installable' : True,
    'aplication' : True,
}