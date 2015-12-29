# -*- coding: utf-8 -*-
{
    "name": "Discounts on Sale Order",
    'version': '8.0.0.0.0',
    'category': 'Sales Management',
    'sequence': 14,
    'author':  'Simone Cittadini',
    'website': 'www.sig-c.com',
    'license': 'AGPL-3',
    'summary': '',
    "description": """
Discounts on Sale Order
=======================
Allows you to define global or line discounts to sale orders by percentage or fixed amount.
    """,
    "depends": [
        "sale",
    ],
    'external_dependencies': {
    },
    "data": [
        'wizard/sale_global_discount_wizard_view.xml',
        'views/sale_order_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
