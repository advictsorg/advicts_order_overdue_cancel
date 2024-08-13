# -*- coding: utf-8 -*-
{
    'name': "Advicts Order Overdue Cancel",
    'summary': """ Automatically cancel orders and invoices after 7 days """,
    'description': """ Automatically cancel orders and invoices after 7 days """,
    'author': "GhaithAhmed@Advicts",
    'website': "https://advicts.com",
    'category': 'Sale',
    'version': '1.0',
    'depends': ['base', 'sale', 'account', 'stock'],
    'data': [
        'data/ir_cron_data.xml',
        'views/settings.xml',
    ],
}
