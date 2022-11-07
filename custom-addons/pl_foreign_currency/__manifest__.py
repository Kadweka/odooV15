# -*- coding: utf-8 -*-
{
    'name': "aa - Multi Currency Partner Ledger",
    'summary': """Partner Ledger report catering for multiple currency transactions""",
    'author': "erp cloud llc",
    'website': "https://www.erpxcloud.com",
    'license':  "Other proprietary",
    'category': 'Accounting',
    'version': '12.0.1.0',
    'depends': ['base', 'account'],
    'data': ['wizard/account_report_partner_ledger_view.xml',
             'report/report_partnerledger.xml'],
    'images':  ["static/description/image.png"],
    'price': 80,
    'currency' :  'EUR',
    'installable': True
}
