#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math
from datetime import *
import openerp
from openerp import api, tools, exceptions
#from datetime import datetime, timedelta
from dateutil import parser
import os
import openerp.modules as addons
import base64
import os
import sys
import platform
import time
from phpserialize import serialize, unserialize
import random
import textwrap
import hashlib

    
def php_is_numeric(var):
        try:
            float(var)
            return True
        except ValueError:
            return False
    
def php_explode(cadena, delimitador, limite=0):
        """Divide una cadena en varias cadenas"""
        cadena = str(cadena)
        delimitador = str(delimitador)
        
        valores = None
        if len(cadena) > 0:
            if limite > 0:
                valores = cadena.split(delimitador, limite)
            else:
                valores = cadena.split(delimitador)
        else:
            valores = [cadena]
            
        return valores
    
def explode(cadena, delimitador, limite=0):
        return php_explode(cadena, delimitador, limite)
    
def php_strpos(cadena, buscar, empezar_en=None):
        """Encuentra la posición de la primera ocurrencia de un substring en un string"""
        """returns -1 when not found:"""
        
        cadena = str(cadena)
        
        pos = -1
        if empezar_en != None and empezar_en > 0:
            pos = cadena.find(buscar, empezar_en)
        else:
            pos = cadena.find(buscar)    
        return pos
    
def php_trim(cadena):
        return cadena.strip()
    
def trim(cadena):
        return php_trim(cadena)
    
def microtime():
        return datetime.now().microsecond
    
def php_serialize(diccionario):
        str = serialize(diccionario)
        return str
    
def php_unserialize(cadena):
        dicc = unserialize(cadena)
        return dicc
    
def php_substr(cadena, leftpos, rightpos):
        'Encuentra la primera aparición de un string'        
        return cadena[leftpos:rightpos] 
    
def substr(cadena, leftpos, rightpos):
        return php_substr(cadena, leftpos, rightpos)
    
def strlen(cadena):
        return len(cadena)
    
def php_strtolower(cadena):
        return cadena.lower()
    
def strtolower(cadena):
        return php_strtolower(cadena)
    
def php_str_replace(search, replace, subject, count=None):
        return subject.replace(search, replace, count)
    
def str_replace(search, replace, subject, count=None):
        return php_str_replace(search, replace, subject, count)
    
def base64_encode(cadena):
        return base64.b64encode(cadena)
        
def base64_decode(cadena):
        return base64.b64decode(cadena)
    
def mt_srand(n):
        return os.urandom(n)
    
def md5(cadena):
        a = hashlib.md5()
        a.update(cadena)
        return a.hexdigest()
    
def php_is_array(dicc):
        return dicc is {} 
    
def is_array(dicc):
        return php_is_array(dicc)
    
def php_time():
        return time.time()
    
def php_wordwrap(cadena, tamano=75, fin_cadena='\n', cut=False):
        #nueva = cadena[0:tamano] + fin_cadena
        #return nueva
        lista = textwrap.wrap(cadena, tamano)
        
        nueva = ''    
        for item in lista:
            nueva += item + fin_cadena
        
        return nueva  
    
def microtime2():
        #return datetime.now().microsecond
        return time.time()
    
def convert_number_to_words(number):
        """Convertir numeros a letras"""
        
        hyphen = '-'
        conjunction = ' Y '
        separator = ', '
        negative = 'NEGATIVO '
        decimal = ' CON '
        dictionary = {}
        dictionary[0] = 'CERO'
        dictionary[1] = 'UNO'
        dictionary[2] = 'DOS'
        dictionary[3] = 'TRES'
        dictionary[4] = 'CUATRO'
        dictionary[5] = 'CINCO'
        dictionary[6] = 'SEIS'
        dictionary[7] = 'SIETE'
        dictionary[8] = 'OCHO'
        dictionary[9] = 'NUEVE'
        dictionary[10] = 'DIEZ'
        dictionary[11] = 'ONCE'
        dictionary[12] = 'DOCE'
        dictionary[13] = 'TRECE'
        dictionary[14] = 'CATORCE'
        dictionary[15] = 'QUINCE'
        dictionary[16] = 'DIECISÉIS'
        dictionary[17] = 'DIECISIETE'
        dictionary[18] = 'DIECIOCHO'
        dictionary[19] = 'DIECINUEVE'
        dictionary[20] = 'VEINTE'
        dictionary[30] = 'TREINTA'
        dictionary[40] = 'CUARENTA'
        dictionary[50] = 'CINQUENTA'
        dictionary[60] = 'SESENTA'
        dictionary[70] = 'SETENTA'
        dictionary[80] = 'OCHENTA'
        dictionary[99] = 'NOVENTA'
        dictionary[100] = 'CIEN'
        dictionary[200] = 'DOSCIENTOS'
        dictionary[300] = 'TRESCIENTOS'
        dictionary[400] = 'CUATROCIENTOS'
        dictionary[500] = 'QUINIENTOS'
        dictionary[600] = 'SEISCIENTOS'
        dictionary[700] = 'SETECIENTOS'
        dictionary[800] = 'OCHOCIENTOS'
        dictionary[900] = 'NOVECIENTOS'
        dictionary[1000] = 'MIL'
        dictionary[1000000] = 'MILLON'
        dictionary[1000000000] = 'BILLON'
        dictionary[1000000000000] = 'TRILLON'
        dictionary[1000000000000000] = 'quadrillion'
        dictionary[1000000000000000000] = 'quintillion'    
        
        if not php_is_numeric(number):
            return "Numero no valido" 
    
    #    if not (0 < number < 999999999):
    #        return 'No es posible convertir el numero a letras'
        
        if number < 0:
            return negative + convert_number_to_words(abs(number));
        
        string = fraction = None;
        
        if php_strpos(number, '.', empezar_en=None) != -1:
            valores = explode(number, '.')
            number = int(valores[0])
            fraction = int(valores[1])
        
        if True:
            if number == 0:
                string = dictionary[int(number)]
            
            elif number < 21:
                string = dictionary[number]
                
            elif number < 100:
                tens = (int) (number / 10) * 10
                units = number % 10
                string = dictionary[tens];
                if (units):
                    string = string + conjunction + dictionary[units]
                        
            elif number < 1000:
                #hundreds  = number / 100;            
                #remainder = number % 100;            
                #string = dictionary[hundreds] + ' ' + dictionary[100]
                
                remainder = number % 100;
                hundreds = number - remainder
                string = dictionary[hundreds]
                
                if remainder:
                    string = string + conjunction + convert_number_to_words(remainder)
                
            else:
                baseUnit = pow(1000, math.floor(math.log(float(number), 1000)));
                numBaseUnits = int(float(number) / baseUnit);
                remainder = float(number) % baseUnit;
                
                #string = convert_number_to_words(numBaseUnits) + ' ' + dictionary[baseUnit];
                string = ' ' + dictionary[baseUnit]
                
                if remainder:
                    if remainder < 100:
                        string = string + conjunction
                    else:
                        string = string + separator
                        string = string + convert_number_to_words(remainder)
        
        contiene_pesos = explode(string, ' PESOS ')
        if contiene_pesos.__len__() == 1:
            string = string + ' PESOS '
        
        if fraction != None and php_is_numeric(fraction) and fraction > 0:
            string = string + decimal
            for number in explode(str(fraction)):
                #string = string + dictionary[int(number)]
                number = int(number)
                
                if number == 0:
                    string += dictionary[int(number)]
                
                elif number < 21:
                    string += dictionary[number]
                    
                elif number < 100:
                    tens = (int) (number / 10) * 10
                    units = number % 10
                    string += dictionary[tens];
                    if (units):
                        string = string + conjunction + dictionary[units]
                            
                elif number < 1000:
                    hundreds = number / 100;
                    remainder = number % 100;
                    string += dictionary[hundreds] + ' ' + dictionary[100]
                    if remainder:
                        string = string + conjunction + convert_number_to_words(remainder)
                    
                else:
                    baseUnit = pow(1000, math.floor(math.log(float(number), 1000)));
                    numBaseUnits = int(float(number) / baseUnit);
                    remainder = float(number) % baseUnit;
                    
                    #string = convert_number_to_words(numBaseUnits) + ' ' + dictionary[baseUnit];
                    string += ' ' + dictionary[baseUnit]
                    
                    if remainder:
                        if remainder < 100:
                            string = string + conjunction
                        else:
                            string = string + separator
                            string = string + convert_number_to_words(remainder)
                
                  
            string = string + ' CENTAVOS'
    
        return string
    
    
def date_operation(date_start, date_end, operation='-'):  
        data = 0
        
        if operation == '-':
            date1 = datetime.strptime(date_start, get_DATETIME_FORMAT())
            date2 = datetime.strptime(date_end, get_DATETIME_FORMAT())
            
            resultado = date2 - date1
            days = resultado.days
            
            horas = resultado.seconds / 60 / 60
            
            if horas > 0:
                data = days + 1 / float(horas)
            else:
                data = days
            
    #        if resultado.days > 0:
    #            days = resultado.days
    #        else:
    #            horas = resultado.seconds / 60
    #            if horas > 0:
    #                days = days + 1 / float(horas)
            
        return data
    
def getDateRange(begin, end):
        """  """
        beginDate = parser.parse(begin)
        endDate = parser.parse(end)
        delta = endDate - beginDate
        numdays = delta.days + 1
        dayList = [datetime.strftime(beginDate + timedelta(days=x), get_DATE_FORMAT()) for x in range(0, numdays)]
        return dayList
    
def get_rango_horas():    
        t = []
        for hora in range(24):
            item = None
            if hora < 10:
                item = ('0' + str(hora) + ':00', '0' + str(hora) + ':00')
            else:
                item = (str(hora) + ':00', str(hora) + ':00')
                
            t.append(item)
        return t
     
     
def fecha_quitar_UTC(fecha):
        temp = parser.parse(fecha)
         
        return temp.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
def get_logo(): 
        return os.path.join(addons.get_module_path('df_dietas'), 'static', 'src', 'img', 'logo_reporte.jpg')
    
def get_DATE_FORMAT():
        return openerp.tools.misc.DEFAULT_SERVER_DATE_FORMAT
    
def get_DATETIME_FORMAT():
        return openerp.tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
    
    #------------------------------
import uuid
def get_mac():
        #mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        #mac = '-'.join(mac_num[i : i + 2] for i in range(0, 11, 2))
        
        for i in xrange(3):
            mac_num = hex(i).replace('0x', '').upper()
            mac = '-'.join(mac_num[i : i + 2] for i in range(0, 11, 2))
            print mac
    
def get_mac2():
        return (':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8 * 6, 8)][::-1])).upper()
    
    
    #------------------------------
def es_multiplo(x, n):
        flag = False if x % n > 0 else True    
        return flag
    
    #------------------------------
def get_os_linebreak():
        return "\r\n"   
    
    #------------------------------
def convertir_fecha(cadena, formato):
        fecha = datetime.strptime(cadena, get_DATETIME_FORMAT())
        return fecha 
    
#-------------------------------
def get_fecha_hoy():
        hoy = time.strftime('%Y-%m-%d')
        return datetime.strptime(hoy, '%Y-%m-%d')


#-------------------------------
def hora2string(hora):    
    import datetime
    td = datetime.timedelta(hours=hora)
    hora_string = (datetime.datetime(2000, 1, 1) + td).strftime("%I:%M")
    hora_string = str(hora_string)
    
    if int(hora) < 12:
        hora_string += ' AM'
    else:
        hora_string += ' PM'
    
    return str(hora_string)

#-------------------------------
import locale
def number_format(num, places=0):
    return locale.format("%.*f", (places, num), True)
