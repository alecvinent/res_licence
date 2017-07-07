# -*- coding: utf-8 -*-

{
    'name': 'Cain',
    'summary': 'Licencias',
    'description': u'Gestor de licencias de módulos Odoo',
    'author': 'Alexander Vinent Peña',
    'licence': 'Other proprietary',
    'website': 'http://www.desoft.cu/scu',
    'category': 'Technical Settings',
    'version': '1.1',
    'depends': ['utiles'],
    'external_dependencies' : {
    },
    'data': [
         #views
         'views/res_licence_view.XML',
         
         'views/menu.xml'
    ],
    'demo': [],
    'application': False    
}
