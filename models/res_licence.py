# -*- coding: utf-8 -*-
import openerp
from openerp import models, fields, api, tools, exceptions
import time
import logging
from openerp import SUPERUSER_ID
_logger = logging.getLogger(__name__)
from licencia import GET_STATES, generate_key, degenerate_key, validate, STATES_OK, STATES_NOT_VALID, STATES_EXPIRED
from openerp.addons.utiles.models.UtilesModel import date_operation

OTROS_DATOS = {}
OTROS_DATOS['proveedor'] = 'DESOFT Santiago de Cuba'
OTROS_DATOS['version'] = '1.0'
TOTAL_CAMPOS_EXTRAS = len(OTROS_DATOS) 


MODULE_NAME = 'res.licence'
class res_licence(models.Model):
    _name = MODULE_NAME  
    _description = "Licencias"
    _rec_name = 'modulo'
    
    #------------------------------------
    def init(self, cr):
        cr.execute("UPDATE res_currency SET active=true WHERE active = false")
        #self.currency_id = 70 #CUP
    
    #------------------------------------
    def _generate(self):
        #if self.semilla:
        #    raise exceptions.ValidationError(u'Esta opción no está disponible.')
        
        OTROS_DATOS['proveedor'] = self.proveedor or OTROS_DATOS['proveedor']
        OTROS_DATOS['version'] = self.version or self.modulo.installed_version
        return generate_key(self.modulo.name, self.env.user.company_id.name, OTROS_DATOS)
    
    #------------------------------------
    def _degenerate(self):
        return degenerate_key(self.semilla, TOTAL_CAMPOS_EXTRAS)
    
    def _validate_key(self):
        try:
            self.semilla = self._generate()
        except Exception, e:
            raise exceptions.ValidationError(u'La licencia no es válida.')
        
    #------------------------------------
    #@api.onchange('semilla_clave')
    def _onchange_semilla_clave(self):
        if self.semilla_clave:
            self.semilla = self.semilla_clave            
        self.semilla_clave = ''
            
    #-------------------------------------
    @api.onchange('semilla')
    @api.depends('semilla')
    @api.one
    def _compute_semilla(self):
        if self.semilla:
            self.dias_restantes = -1
            try:
                self.state = validate(self.semilla, TOTAL_CAMPOS_EXTRAS)
                
                datos = self._degenerate()
                if 'L2' in datos:
                    self.desde = datos['L2']
                
                if 'L3' in datos:
                    self.vence = datos['L3']
                    
                if 'L6' in datos:
                    self.dias_restantes = date_operation(datos['L2'], datos['L3']) - 1
                
                    if self.dias_restantes <= 0:
                        self.state = STATES_EXPIRED
            except Exception, e:
                self.state = STATES_NOT_VALID
                #raise exceptions.ValidationError(u'La licencia no es válida.')
    
    #------------------------------------       
    @api.onchange('modulo', 'proveedor')
    @api.one
    def _onchange_datos(self):
        if self.modulo and self.proveedor:
            self.version = self.modulo.installed_version
            self.proveedor = self.modulo.author
            self._regenerar_key()
            
    #----------------
    @api.one
    def _inverse_state(self):
        self.state = self.state
    
    #------------------------------------
    company_id = fields.Many2one('res.company', 'Entidad', default=lambda self: self.env.user.company_id.id)
    semilla = fields.Text("Licencia", help='Licencia actual', readonly=True)
    semilla_clave = fields.Text("Nueva licencia", help='Nueva licencia')
    modulo = fields.Many2one('ir.module.module', u'Aplicación', required=True, readonly=True)
    proveedor = fields.Char("Proveedor", default=OTROS_DATOS['proveedor'], readonly=True)
    version = fields.Char(u"Versión", readonly=True)
    desde = fields.Date('Inicio', compute='_compute_semilla')  
    vence = fields.Date('Vence', compute='_compute_semilla')    
    state = fields.Selection(GET_STATES(), string='Estado', default='OK', compute='_compute_semilla', inverse='_inverse_state')
    dias_restantes = fields.Integer(u'Días restantes', default='-1', compute='_compute_semilla')
    
    #------------------------------------
    _sql_constraints = [
        
    ]
    
    #------------------------------------
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u"%s %s" % (u'Módulo', record.modulo.shortdesc)
                ))
        return result
    #------------------------------------
    @api.one
    @api.constrains('company_id', 'modulo', 'proveedor')
    def _check_registration(self):
        domain = [('company_id', '=', self.company_id.id), ('modulo', '=', self.modulo.name), ('proveedor', '=', self.proveedor)]
        existe = self.search_count(domain)
        if existe > 0:
            raise exceptions.ValidationError(u'Ya se ha registrado ese módulo.')
    
    #------------------------------------
    @api.model
    def create(self, vals):
        row = super(res_licence, self).create(vals)     
        
        OTROS_DATOS['proveedor'] = row.proveedor or OTROS_DATOS['proveedor']
        OTROS_DATOS['version'] = row.version or row.modulo.installed_version
        
        semilla = generate_key(row.modulo.name, row.env.user.company_id.name, OTROS_DATOS)   
        row.semilla = semilla
        
        return row
    
    #------------------------------------
    @api.multi
    def write(self, vals):
        if not 'semilla_clave' in vals and 'semilla' not in vals:
            #no se puede instalar si no esta 'abel'
            domain = [('name', '=', 'res_licence_abel')]        
            existe = self.env['ir.module.module'].search_count(domain)
            if existe == 0:
                raise exceptions.ValidationError(u'Esta opción no está disponible.')
        elif 'semilla_clave' in vals:
            vals['semilla'] = vals['semilla_clave']
            vals['semilla_clave'] = ''
            
        return super(res_licence, self).write(vals)
    
    #------------------------------------
    @api.multi
    def unlink(self):
        #no se puede instalar si no esta 'abel'
        domain = [('name', '=', 'res_licence_abel')]        
        existe = self.env['ir.module.module'].search_count(domain)
        if existe == 0:
            raise exceptions.ValidationError(u'Esta opción no está disponible.')
        
        return super(res_licence, self).unlink()
            
        
    #------------------------------------
    @api.multi
    def _regenerar_key(self):
        self.semilla = self._generate() 
        #self.semilla_clave = self._degenerate()
        self._do_reopen_form()
    
    #------------------------------------
    @api.multi
    def _do_reopen_form(self):
        self.ensure_one()
        return {  
            'type': 'ir.actions.act_window',
            'res_model': self._name, # this model 
            'res_id': self.id, # the current wizard record 
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }
    
    #------------------------------------
    def validar(self, modulo):         
        #existing_move = registry['account.move'].search(cr, SUPERUSER_ID, [('tax_cash_basis_rec_id', '!=', False)])
        domain = [('name', '=', modulo)]
        modulo_id = self.env['ir.module.module'].search(domain, limit=1)
        
        if not modulo_id:
            raise exceptions.ValidationError(u'El módulo ' + modulo + ' no está instalado o no existe.')        
        
        domain = [('modulo', '=', modulo_id.id)]
        licencia = self.search(domain, limit=1)
        
        if not licencia:
            raise exceptions.ValidationError(u'La licencia del módulo ' + modulo + u' es inválida.')
            
        state = validate(licencia.semilla, TOTAL_CAMPOS_EXTRAS)
        estados = GET_STATES()
        if state != STATES_OK: 
            raise exceptions.ValidationError(u'La licencia del módulo ' + modulo + ' ' + state)
        else:
            if licencia.dias_restantes <= 0:
                raise exceptions.ValidationError(u'La licencia ha vencido. Copie la licencia actual y envíela a su proveedor.')
            
        
    #------------------------------------
    def generar_licencia(self, cr, registry, modulo):   
        domain = [('name', '=', modulo)]
        module_ids = registry['ir.module.module'].search(cr, SUPERUSER_ID, domain)
        modulo_id = registry['ir.module.module'].browse(cr, SUPERUSER_ID, module_ids)
        
        if not modulo_id:
            raise exceptions.ValidationError(u'El módulo ' + modulo + ' no está instalado o no existe.')        
        
        domain = [('modulo', '=', modulo_id.id)]
        existe = registry[MODULE_NAME].search(cr, SUPERUSER_ID, domain)
        if len(existe) == 0:
            data = {
                'modulo': modulo_id.id,
                'version': modulo_id.installed_version,
                'proveedor': modulo_id.author
            }
                 
            registry[MODULE_NAME].create(cr, SUPERUSER_ID, data, context=None)
        
    #------------------------------------
    @api.one
    def regenerar_key(self):
        self._regenerar_key()
        
    #------------------------------------
res_licence()
