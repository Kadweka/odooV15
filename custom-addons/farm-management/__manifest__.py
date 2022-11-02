{
    'name': 'Open Farm Management',
    'version': '15.0.1.0.0',
    'summary': 'Manage Farm Activities',
    'description': """
        Helps you to manage Farm Daily activities.
        """,
    'category': 'Generic Modules',
    'author': "@The-Kadweka & Kiro",
    'company': 'BroadSpace Interactive',
    'maintainer': 'BroadSpace Interactive',
    # 'live_test_url': 'https://youtu.be/lAT5cqVZTZI',
    'website': "https://broadspaceinteractive.com/",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/land_view.xml',
        'views/block_view.xml'
    ],
    'images': ['static/description/logo.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
