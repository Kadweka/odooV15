# -*- coding: utf-8 -*-
{
    'name': "Adc Memo",

    'summary': """
        Adc Memo""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_expense', 'ohrms_loan', 'employee_vehicle_request'],

    # always loaded
    'data': [
        'reports/expense_memo.xml',
        'reports/loan_memo.xml',
        'reports/report.xml',
        'reports/vehicle_request_memo.xml',
    ]
}
