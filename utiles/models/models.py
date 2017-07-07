# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_company(models.Model):
    _inherit = "res.company"
    
    #------------------------------------
    def init(self, cr):
        cr.execute("UPDATE res_currency SET active=true WHERE active = false")        
    
    #------------------------------------
res_company()

#------------------------------------
#------------------------------------
class res_lang(models.Model):
    _inherit = "res.lang"
    
    #------------------------------------
    def init(self, cr):
        #modificar separador decimales y miles        
        cr.execute("UPDATE res_lang SET thousands_sep=',', decimal_point='.' WHERE code = 'es_ES'")
        
    
    #------------------------------------
res_lang()