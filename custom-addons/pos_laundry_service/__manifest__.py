# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-Today Geminate Consultancy Services (<http://geminatecs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": 'POS Laundry Service',
    "version": '15.0.0.1',
    "category": 'Point of Sale',
    "author": 'Geminate Consultancy Services',
    "website": 'http://www.geminatecs.com"',
    "summary": "Geminate comes with a vertical solution for the laundry industry which integrates with Point of Sale to provide an interface for key in laundry orders.",
    "description": """
                                Geminate comes with a vertical solution for the laundry industry which integrates with Point of Sale to provide an interface for key in laundry orders. different type of options available while handling laundry orders like,
                                1. Various types of services like 'Wash only', 'Iron only', 'Wash and Iron Both'.
                                2. Various types of washing stages during the laundry process.
                                3. Urgent orders are supported with additional charges.
                                4. Home delivery support with additional charges.
                                5. Separate accounting maintained for urgent order and home delivery charges.
                                6. Multiple roles available like laundry boy, dry cleaner and delivery boy which we can assign them on their related job during the laundry process.
                                7. Track the time taken for washing and ironing those laundry orders.
                                8. Easy user management based on different roles and access restrictions to the laundry system.
                            """,
    "depends": ['base', 'point_of_sale', 'sale', 'sale_management', 'account'],
    "license": 'Other proprietary',
    "data": [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/point_of_sale.xml',
        'views/aces_pos_note.xml',
        'views/account.xml',
        'views/sale_order.xml',
        'views/washing_view.xml',
        'views/pos_config_view.xml',
        'views/res_partner_views.xml',
        'report/account_invoice_report.xml',
        'report/sale_order_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_laundry_service/static/src/css/radio_button.css',
            'pos_laundry_service/static/src/js/WashingStageButton.js',
            'pos_laundry_service/static/src/js/IsUrgent.js',
            'pos_laundry_service/static/src/js/WashingStagePopupWidget.js',
            'pos_laundry_service/static/src/js/washing_error_popup.js',
            'pos_laundry_service/static/src/js/SelectClothPopupWidget.js',
            'pos_laundry_service/static/src/js/SelectNullPopupWidget.js',
            'pos_laundry_service/static/src/js/orderline.js',
            'pos_laundry_service/static/src/js/addnotepopup.js',
            'pos_laundry_service/static/src/js/ProductNotePopupWidget.js',
        ],
        'web.assets_qweb': [
            'pos_laundry_service/static/src/xml/*.xml',
        ],
    },
    "qweb": ['pos_laundry_service/static/src/xml/*.xml'],
    "images": ['static/description/banner.png'],
    "installable": True,
    "auto_install": False,
    "application": True,
    'price': 99.99,
    'currency': 'USD'
}
