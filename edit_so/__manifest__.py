{
    'name': 'Edit SO',
    'version': 'Version',
    'category': 'Category',
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'depends': [
        'base',
        'sale',
        'sale_management',
        'sales_team',
        'edit_po',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/unlimited_discount_group.xml',
        'report/sale_order_report.xml',
        'views/sale_order_line.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'auto_install': False
}
