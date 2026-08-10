# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Extra Fields',
    'version': '16.0.1.0.0',
    'summary': 'Add two extra fields to Sales Order, after the Customer field',
    'description': 'Adds two custom Char fields (Extra Field 1, Extra Field 2) to the '
                    'Sales Order form view, placed right after the Customer field.',
    'category': 'Sales',
    'author': 'My Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
