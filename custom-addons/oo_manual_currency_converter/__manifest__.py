# -*- coding: utf-8 -*-
{
    'name': "Manual Currency Converter",

    'summary': """
        Add a manual exchange rate when making payments from any currency!""",

    'description': """
        Long description of module's purpose
    """,

    'author': "@the-macharia",
    'website': "http://www.yourcompany.com",

    'category': 'Account',
    'version': '13.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'views/account.xml',
    ]
}
