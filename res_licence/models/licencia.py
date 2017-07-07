# -*- coding: utf-8 -*-
# encoding=utf8

import logging
_logger = logging.getLogger(__name__)

from datetime import *
import hashlib
import base64
from openerp.addons.utiles.models.UtilesModel import *

##############################
#para errores de codificacion
import sys
reload(sys)
sys.setdefaultencoding('utf8')

##############################

BEGIN1 = '-------------------------------BEGIN LICENSE KEY--------------------------------'
END1 = '--------------------------------END LICENSE KEY---------------------------------'

_LINEBREAK = get_os_linebreak ()

#wrap key settings
_WRAPTO = 50
_PAD = "-"
_MAC = ''

TOTAL_CAMPOS = 5

#* id 1 used to validate license keys
#* id 2 used to validate license key requests
#* id 3 used to validate dial home data

#// id to check for to validate source
ID1 = 'nSpkAHRiFfM2hE588eB';
ID2 = 'NWCy0s0JpGubCVKlkkK';
ID3 = 'G95ZP2uS782cFey9x5A';

TOTAL_BYTES = 'h0lamund'
FILL = '*'

# MAC
L1 = ''

#inicio
L2 = ''

#fin
L3 = ''

#sistema
L4 = ''

#entidad
L5 = ''

#intervalo restante
L6 = -1

INTERVALO = 60

#---------------------------------------------
def generate_key(modulo, entidad, otros_datos={}):      
    L1 = get_mac2()
    L2 = get_fecha_hoy()   
    L3 = L2 + timedelta(days=INTERVALO)
    L4 = modulo
    L5 = entidad
    
    L1_c = encrypt_DES(L1)
    L2_c = encrypt_DES(str(L2))
    L3_c = encrypt_DES(str(L3))
    L4_c = encrypt_DES(L4)
    L5_c = encrypt_DES(L5)
    
    
    cadena = L1_c + _LINEBREAK
    cadena += L2_c + _LINEBREAK
    cadena += L3_c + _LINEBREAK
    cadena += L4_c + _LINEBREAK
    cadena += L5_c + _LINEBREAK
    
    for key in otros_datos.keys():
        L = unicode(otros_datos[key])
        L_c = encrypt_DES(L)                
        cadena += L_c + _LINEBREAK
    
    i = 0
    while i < TOTAL_CAMPOS:
        cadena += base64.b64encode(md5(BEGIN1 + str(i))) + _LINEBREAK
        i += 1
    
    crypt = encrypt_DES(cadena)  
    crypt = php_trim(crypt)
    
    cadena = BEGIN1 + _LINEBREAK + php_wordwrap (crypt, _WRAPTO, _LINEBREAK, 1) + END1
    
    return unicode(cadena)

#---------------------------------------------
def degenerate_key(cadena, total_campos=0):    
    plain = {}
    
    cadena_new = cadena.replace(BEGIN1, '')
    cadena_new = cadena_new.replace(END1, '')
    cadena_new = cadena_new.replace(_LINEBREAK, '')
    cadena_new = cadena_new.replace('\r', '')
    cadena_new = cadena_new.replace('\n', '')
    cadena_new = cadena_new.replace('\t', '')
    cadena_new = dencrypt_DES(cadena_new)
    
    partes = explode(_LINEBREAK, cadena_new, 0) 
    try:
        for parte in partes:
            partes.remove('')
    except:
        pass
    
    try:
        for parte in partes:
            i = 0
            while i < TOTAL_CAMPOS:
                partes.remove(base64.b64encode(md5(BEGIN1 + str(i))))
                i += 1
    except:
        pass
    
    campos = TOTAL_CAMPOS + total_campos
    if len(partes) == campos:
        i = 0
        while i < campos:
            L_c = dencrypt_DES(partes[i])
            plain['L' + str(i + 1)] = L_c
            i += 1
    
    return plain

#--------------------------------------------- para usar DES debe ser multiplo de 8
def encrypt_DES(plain):
    return base64.b64encode(base64.b64encode(plain))

#---------------------------------------------
def dencrypt_DES(cadena):
    return base64.b64decode(base64.b64decode(cadena))

#---------------------------------------------
STATES = {}
STATES_OK = 'OK'
STATES_NOT_VALID = 'NOT VALID'
STATES_EXPIRED = 'EXPIRED'

STATES[STATES_OK] = 'OK'
STATES[STATES_NOT_VALID] = u'Licencia inválida'
STATES[STATES_EXPIRED] = u'La licencia ha vencido. Copie la licencia actual y envíela a su proveedor.'

def validate(licencia, total):
    msg = STATES_OK
        
    a = TOTAL_CAMPOS + total
    #
    key = degenerate_key(licencia, total)
    if len(key) != a:
        msg = STATES_NOT_VALID
    elif key['L1'] != get_mac2():
        msg = STATES_NOT_VALID
    else:
        hoy = get_fecha_hoy()
        vence = convertir_fecha(key['L3'], 'formato')
        
        if hoy > vence:
            msg = STATES_EXPIRED
    
    return msg

#------------------------------------
def GET_STATES():
    lista = []
    
    for key in STATES.keys():
        a = (key, STATES[key])
        lista.append(a)        
    
    return lista
#------------------------------------
