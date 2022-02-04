# -*- coding: utf-8 -*-
{
    'name': "school Prueba",

    'summary': """
        Es mi primer modulo de prueba para Odoo14""",

    'description': """
        Este modulo de prueba servira para gestion de centros educativos
    """,

    'author': "DanielALQ",
    'website': "http://www.mipagina.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Modulo de pruebas',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
