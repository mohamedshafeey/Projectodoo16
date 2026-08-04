# -*- coding: utf-8 -*-
{
    'name': 'Custom',
    'version': '16.0.1.0.0',
    'summary': 'Add Date field to Sales Order',
    'description': 'Adds a custom "Date" field (Char) to the Sales Order form and tree views.',
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
