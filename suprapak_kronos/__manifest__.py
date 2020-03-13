# -*- coding: utf-8 -*-
{
    'name': "Kronos",

    'summary': "",

    'description': "This is a module for Suprapak",

    'author': "Todoo",
    'website': "http://www.todoo.co",
    'contributors': "Livingston Arias la@todoo,co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_crm','mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/data_sheet_view.xml',
        'views/data_sheet_menu.xml',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
