# -*- coding: utf-8 -*-

{
    'name' : 'Pagos de facturas',
    'version' : '1.0',
    'category': 'Uncategorized',
    'author' : 'TakanaGS',
    'website': "http://www.takanags.com/dev",
    'summary' : 'Gestiona los pagos de las facturas',
    'description' : 'Gestiona los pagos de las facturas',
    'depends' : [
                'base',
                'account',
                ],
    'data' : [
            'security/pacifico_payment_security.xml',
            'security/ir.model.access.csv',
            'pacifico_payment_invoice_view.xml',
            'res_partner_view.xml',
            'account_invoice_view.xml',
            'views/pacifico_payment_layouts.xml',
            ],
    'installable' : True,
    'aplication' : True,
}
