1. Para usar el generador de licencias en su proyecto, agregue 
	la linea siguiente en el fichero '__openerp__py':

	'depends': ['res_licence'],
	'post_init_hook': '_check_script'

2. En el fichero '__init__.py' de su módulo, agregue la siguiente función:

	def _check_script(cr, registry):
    	registry['res.licence'].generar_licencia(cr, registry, 'mi_modulo')
    	return
	
3. Para chequear la licencia, agregue la siguiente línea en su proyecto:
  
	self.env['res.licence'].validar('mi_modulo')
	
	Por ejemplo:
	En este caso se hace un chequeo de la licencia antes de crear un elemento. Si no es correcta,
	se genera una excepción, impidiendon ejecutar el resto de su código.
	
	@api.model
    def create(self, vals):
    	self.env['res.licence'].validar('mi_modulo')
        return super(mi_modelo, self).create(vals)