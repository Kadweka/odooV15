{
    'name': 'Three Factors Approvers',
    'summary': """This module will add do all customizations for odoo""",
    'version': '15.0.1.0.0',
    'description': """This module will add do all customizations for odoo""",
    'author': '@The-Kadweka',
    'company': 'BroadSpace Interactive',
    'website': 'https://broadspaceinteractive.com',
    'category': 'Tools',
    'depends': ['base','hr_contract','hr','hr_expense','hr_holidays'],
    'license': 'AGPL-3',
    'data': [
       "views/approvers_view.xml",
       "security/security.xml",
    #    'reports/expense_report.xml',
       'views/expense_view.xml'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}