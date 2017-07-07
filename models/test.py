# -*- coding: utf-8 -*-

from openerp.addons.utiles.models.UtilesModel import *

#-------------------------------------------------
BEGIN1 = '-------------------------------BEGIN LICENSE KEY--------------------------------'
END1 = '--------------------------------END LICENSE KEY---------------------------------'

BEGIN2 = '_DATA{'
END2 = '}DATA_'

SEEDS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890123456789'

#hash key 1 used to encrypt the generate key data.
HASH_KEY1 = 'YmUzYWM2sNGU24NbA363zA7IDSDFGDFGB5aVi35BDFGQ3YNO36ycDFGAATq4sYmSFVDFGDFGps7XDYEzGDDw96OnMW3kjCFJ7M+UV2kHe1WTTEcM09UMHHT'

#hash key 2 used to encrypt the request data
HASH_KEY2 = '80dSbqylf4Cu5e5OYdAoAVkzpRDWAt7J1Vp27sYDU52ZBJprdRL1KE0il8KQXuKCK3sdA51P9w8U60wohX2gdmBu7uVhjxbS8g4y874Ht8L12W54Q6T4R4a'

#hash key 3 used to encrypt the dial home data
HASH_KEY3 = 'ant9pbc3OK28Li36Mi4d3fsWJ4tQSN4a9Z2qa8W66qR7ctFbljsOc9J4wa2Bh6j8KB3vbEXB18i6gfbE0yHS0ZXQCceIlG7jwzDmN7YT06mVwcM9z0vy62T'

#wrap key settings
_WRAPTO = 80
_PAD = "-"
_MAC = ''

USE_SERVER = True
USE_TIME = True

#* id 1 used to validate license keys
#* id 2 used to validate license key requests
#* id 3 used to validate dial home data

#// id to check for to validate source
ID1 = 'nSpkAHRiFfM2hE588eB';
ID2 = 'NWCy0s0JpGubCVKlkkK';
ID3 = 'G95ZP2uS782cFey9x5A';

TOTAL_BYTES = 'h0lamund'
FILL = '*'

#---------------------------------
def _get_os():
    return platform.system()

#-----------------------
def _get_python_version():
    return sys.version

#---------------------------------
def _get_os_linebreak ():
    nl = "\r\n"
    
    os = strtolower (_get_os()) 
    
    
    
    return nl

#---------------------------------------------
_LINEBREAK = _get_os_linebreak ()

#---------------
def _generate_random_string(length=10, seeds='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890123456789'):
    cadena = '';
    seeds_count = len(seeds)
        
    valor_random = random.randrange(0, datetime.today().day)
        
    i = 0
    while length > i:
        #str += seeds + mt_srand(seeds_count - 1)
        valor = random.randint(0, datetime.today().day - 1)
        cadena += seeds + str(valor) 
        
        i += 1
    
    return cadena

#---------------
def _get_key(key_type):
    if key_type == 'KEY' :
        return HASH_KEY1
    elif key_type == 'REQUESTKEY':
        return HASH_KEY2
    elif key_type == 'HOMEKEY' :
        return HASH_KEY3

#---------------
def _encrypt(src_array, key_type='KEY'):
    rand_add_on = _generate_random_string(3)
    
    #get the key
    key = _get_key (key_type)
    
    crypt = ''
    str = php_serialize(src_array)
    
    # loop through the str and encrypt it
    i = 1
    while i <= len(str):
        char = php_substr (str, i - 1, 1)
        keychar = php_substr (key, (i % len (key)) - 1, 1)
        
        if len(char) == 0 or len(keychar) == 0:
            i += 1
            continue
        
        valor = ord(char) + ord(keychar)
        a = chr(valor)        
        crypt += a    
        i += 1
    
    # return the key
    return rand_add_on + base64_encode(base64_encode (php_trim (crypt)))
        
    
#------------------------------

def _decrypt(str, key_type='KEY'):
    rand_add_on = php_substr (str, 0, 3)
    str = base64_decode (base64_decode (php_substr (str, 3)))
    
    # get the key
    key = rand_add_on + _get_key (key_type)
    
    decrypt = ''
    
    # loop through the text and decode the string
    i = 1
    while i <= len(str):
        char = php_substr (str, i - 1, 1)
        keychar = php_substr (key, (i % strlen (key)) - 1, 1)
        char = chr (ord (char) - ord (keychar))
        decrypt += char
        
        i += 1

    return php_unserialize(decrypt)
    
#------------------------------
def _pad(str):
    str_len = strlen (str);
    spaces = (_WRAPTO - str_len) / 2;
    str1 = ''
    
    i = 0
    while i < spaces:
        str1 = str1 + _PAD
        i += 1
    
    if spaces / 2 != round (spaces / 2):
        str = substr (str1, 0, strlen (str1) - 1) + str
    else:
        str = str1 + str
        
    str = str + str1
    
    return str

#---------------------------
def _get_begin(key_type):
    #gets the begining license key seperator text
    if key_type == 'KEY':
        return BEGIN1
    elif key_type == 'REQUESTKEY':
        return BEGIN2
    elif key_type == 'HOMEKEY':
        return ''
    
#---------------------------
def _get_end(key_type):
    #gets the end license key seperator text
    if key_type == 'KEY':
        return END1
    elif key_type == 'REQUESTKEY':
        return END2
    elif key_type == 'HOMEKEY':
        return ''

#------------------------
def _wrap_license(src_array, key_type='KEY'):
    #* wraps up the license key in a nice little package
    
    #sort the variables
    begin = _pad (_get_begin (key_type))
    end = _pad (_get_end (key_type))
    
    # encrypt the data
    cadena = _encrypt (src_array, key_type)
    
    #// return the wrap
    return begin + _LINEBREAK + php_wordwrap(cadena, _WRAPTO, _LINEBREAK, 1) + _LINEBREAK + end
    
    
#------------------------------
def _unwrap_license(enc_str, key_type='KEY'):
    #* unwraps license key back into it's data array
    
    #// sort the variables
    begin = _pad (_get_begin (key_type))
    end = _pad (_get_end (key_type))
    
    #// get string without seperators
    dicc = {
        begin,
        end,
        "\r",
        "\n",
        "\t"
    }
    str = trim (str_replace (dicc, '', enc_str));
    
    #// decrypt and return the key
    return _decrypt (str, key_type)
    

_LICENSE_PATH = ''

def _get_mac_address():
    return get_mac2()

def init(use_mcrypt=True, use_time=True, use_server=True, allow_local=False, owner=None, sistema=None):
    _LINEBREAK = _get_os_linebreak ()

def license_application(license_path='license.dat', use_mcrypt=True, use_time=True, use_server=True, allow_local=False, owner=None, sistema=None):
    _LICENSE_PATH = license_path
    
    init (use_mcrypt, use_time, use_server, allow_local, owner, sistema)
    
    if use_server:
        _MAC = _get_mac_address()
        

        
#-------------------------------
def generate(domain='', start=0, expire_in=31449600, other_array={}):
    #generates the server key when the license class resides on the server
    
    DATA = {}
    #// set the id
    DATA ['ID'] = md5 (ID1)
    
    #// set server binds
    if USE_SERVER:
        #// set the domain
        DATA ['SERVER'] = {}
        DATA ['SERVER'] ['DOMAIN'] = domain
        
        #// set the mac id
        DATA ['SERVER'] ['MAC'] = _get_mac_address()
        
    #// set time binds
    if USE_TIME and not is_array (start):
        current = php_time()
        start = start if (current < start) else current + start
        
        #// set the dates
        DATA ['DATE'] = {}
        DATA ['DATE'] ['START'] = start
        DATA ['DATE'] ['SPAN'] = expire_in
        
        if expire_in == 'NEVER':
            DATA ['DATE'] ['END'] = 'NEVER'
        else:
            DATA ['DATE'] ['END'] = start + expire_in
            
    
    #// if start is array then it is the other array and time binding is not in use
    #// convert to other array
    if is_array (start):
        other_array = start
        
    #// set the server os
    other_array ['_PYTHON_OS'] = _get_os()
    
    #// set the server os
    other_array ['_PYTHON_VERSION'] = _get_python_version()
    
    #// merge the data with the other array
    DATA ['DATA'] = other_array
    
    #// encrypt the key
    key = _wrap_license(DATA)
    
    return key
    
#--------------------------
def crear(days=15, fichero_licencia='licence/license.lic', fichero_licencia_backup='images/grid.png'):
    otros_datos = {}
    
    #// convertir a segundos
    hasta = 60 * 60 * 24 * days
    
    #// generate a key with your server details
    #// $gen_key = $architect->generate($variables_servidor['DOMAIN'], $desde, $hasta, $otros_datos);
    gen_key = generate ('DEMO', 0, hasta, otros_datos)
    
    return gen_key
    
#------------------------------
#------------------------------
#------------------------------
#------------------------------
#------------------------------
#------------------------------
import logging
_logger = logging.getLogger(__name__)

from Crypto import Random
from Crypto.Hash import *
from Crypto.Cipher import *

#---------------------------------------------
def generate_key():    
    return crear()
    
    #inicio
    cadena = BEGIN1 + '\n'
    
    #mac
    mac = 'mac:' + get_mac2()   
    coded_mac = encryptar(mac)    
    cadena += coded_mac    
    
    #fin
    cadena += '\n' + END1
    
    return cadena


def encryptar(entrada):
    salida = ''
    
    try:
        salida = encrypt_DES(entrada)
    except Exception, e:
        exceptions.ValidationError('Crypto missing %s' % (e))
    
    return salida

def desencryptar(entrada):
    try:
        from Crypto.Hash import *
    except:
        exceptions.ValidationError('Crypto missing')
    
    salida = dencrypt_DES(entrada)
    return salida

def es_validado(entrada):
    flag = True
    return flag

def encrypt_MD5(cadena):
    m = MD5.new()
    m.update(cadena)
    return m.digest()

def encrypt_DES(cadena):
    cipher = DES.new(SEEDS)
    return cipher.encrypt(cadena).strip()

def dencrypt_DES(cadena):
    cipher = DES.new(SEEDS)
    return cipher.decrypt(cadena).strip()


def cifrado():
    n = cifrado_cesar(_get_mac_address(), 'encrypt')
    
    key = _wrap_license(n) 
    return key

def cifrado_cesar(message, mode='encrypt'):    
    # the string to be encrypted/decrypted 
    #message = 'This is my secret message.'
    
    # the encryption/decryption key
    key = 13 
    
    # tells the program to encrypt or decrypt 
    #mode = 'encrypt' # set to 'encrypt' or 'decrypt' 
    
    # every possible symbol that can be encrypted
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    LETTERS = SEEDS
    
    # stores the encrypted/decrypted form of the message 
    translated = ''
    
    # capitalize the string in message 
    message = message.upper() 
    
    # run the encryption/decryption code on each symbol in the message string
    for symbol in message: 
        if symbol in LETTERS: 
            # get the encrypted (or decrypted) number for this symbol
            num = LETTERS.find(symbol) # get the number of the symbol
            
            if mode == 'encrypt': 
                num = num + key 
            elif mode == 'decrypt': 
                num = num - key
                
            # handle the wrap-around if num is larger than the length of 
            # LETTERS or less than 0
            if num >= len(LETTERS):
                num = num - len(LETTERS)
            elif num < 0: 
                num = num + len(LETTERS)
                
            # add encrypted/decrypted number's symbol at the end of translated
            translated = translated + LETTERS[num] 
            
        else:
            # just add the symbol without encrypting/decrypting 
            translated = translated + symbol
            
    # print the encrypted/decrypted string to the screen
    
    return translated



#--------------------------------
#XTEA Block Encryption Algorithm

""" 
XTEA Block Encryption Algorithm

Author: Paul Chakravarti (paul_dot_chakravarti_at_gmail_dot_com)
License: Public Domain

This module provides a Python implementation of the XTEA block encryption
algorithm (http://www.cix.co.uk/~klockstone/xtea.pdf). 

The module implements the basic XTEA block encryption algortithm
(`xtea_encrypt`/`xtea_decrypt`) and also provides a higher level `crypt`
function which symmetrically encrypts/decrypts a variable length string using
XTEA in OFB mode as a key generator. The `crypt` function does not use
`xtea_decrypt` which is provided for completeness only (but can be used
to support other stream modes - eg CBC/CFB).

This module is intended to provide a simple 'privacy-grade' Python encryption
algorithm with no external dependencies. The implementation is relatively slow
and is best suited to small volumes of data. Note that the XTEA algorithm has
not been subjected to extensive analysis (though is believed to be relatively
secure - see http://en.wikipedia.org/wiki/XTEA). For applications requiring
'real' security please use a known and well tested algorithm/implementation.

The security of the algorithm is entirely based on quality (entropy) and
secrecy of the key. You should generate the key from a known random source and
exchange using a trusted mechanism. In addition, you should always use a random
IV to seed the key generator (the IV is not sensitive and does not need to be
exchanged securely)

    >>> import os
    >>> iv = 'ABCDEFGH'
    >>> z = crypt('0123456789012345','Hello There',iv)
    >>> z.encode('hex')
    'fe196d0a40d6c222b9eff3'
    >>> crypt('0123456789012345',z,iv)
    'Hello There'

""" 

import struct

def esta():
    key = os.urandom(16)
    iv = os.urandom(8)
    data = _get_mac_address()
    
    z = crypt(key, data, iv)
    return z
    

def crypt(key, data, iv='\00\00\00\00\00\00\00\00', n=32):
    """
        Encrypt/decrypt variable length string using XTEA cypher as
        key generator (OFB mode)
        * key = 128 bit (16 char) 
        * iv = 64 bit (8 char)
        * data = string (any length)

        >>> import os
        >>> key = os.urandom(16)
        >>> iv = os.urandom(8)
        >>> data = os.urandom(10000)
        >>> z = crypt(key,data,iv)
        >>> crypt(key,z,iv) == data
        True

    """
    def keygen(key, iv, n):
        while True:
            iv = xtea_encrypt(key, iv, n)
            for k in iv:
                yield ord(k)
    xor = [ chr(x ^ y) for (x, y) in zip(map(ord, data), keygen(key, iv, n)) ]
    return "".join(xor)

def xtea_encrypt(key, block, n=32, endian="!"):
    """
        Encrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) 
        * block = 64 bit (8 char)
        * n = rounds (default 32)
        * endian = byte order (see 'struct' doc - default big/network) 

        >>> z = xtea_encrypt('0123456789012345','ABCDEFGH')
        >>> z.encode('hex')
        'b67c01662ff6964a'

        Only need to change byte order if sending/receiving from 
        alternative endian implementation 

        >>> z = xtea_encrypt('0123456789012345','ABCDEFGH',endian="<")
        >>> z.encode('hex')
        'ea0c3d7c1c22557f'

    """
    v0, v1 = struct.unpack(endian + "2L", block)
    k = struct.unpack(endian + "4L", key)
    sum, delta, mask = 0L, 0x9e3779b9L, 0xffffffffL
    for round in range(n):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + k[sum & 3]))) & mask
        sum = (sum + delta) & mask
        v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + k[sum >> 11 & 3]))) & mask
    return struct.pack(endian + "2L", v0, v1)

def xtea_decrypt(key, block, n=32, endian="!"):
    """
        Decrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) 
        * block = 64 bit (8 char)
        * n = rounds (default 32)
        * endian = byte order (see 'struct' doc - default big/network) 

        >>> z = 'b67c01662ff6964a'.decode('hex')
        >>> xtea_decrypt('0123456789012345',z)
        'ABCDEFGH'

        Only need to change byte order if sending/receiving from 
        alternative endian implementation 

        >>> z = 'ea0c3d7c1c22557f'.decode('hex')
        >>> xtea_decrypt('0123456789012345',z,endian="<")
        'ABCDEFGH'

    """
    v0, v1 = struct.unpack(endian + "2L", block)
    k = struct.unpack(endian + "4L", key)
    delta, mask = 0x9e3779b9L, 0xffffffffL
    sum = (delta * n) & mask
    for round in range(n):
        v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + k[sum >> 11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + k[sum & 3]))) & mask
    return struct.pack(endian + "2L", v0, v1)
#--------------------------------

#transposition

def transposition():
    myMessage = 'Common sense is not so common.' 
    myKey = 8 
    
    begin = _pad ( _get_begin ( 'KEY' ) )
    end = _pad ( _get_end ( 'KEY' ) )
    
    n = transposition_encryptMessage(myKey, myMessage)
    
    a = begin + _LINEBREAK + php_wordwrap ( n, _WRAPTO, _LINEBREAK, 1 ) + _LINEBREAK + end;
    
    return n

def transposition_encryptMessage(key, message):
    # Each string in ciphertext represents a column in the grid. 
    ciphertext = [''] * key
    
    # Loop through each column in ciphertext.
    for col in range(key): 
        pointer = col 
        
        # Keep looping until pointer goes past the length of the message.
        while pointer < len(message): 
            # Place the character at pointer in message at the end of the
            # current column in the ciphertext list. 
            ciphertext[col] += message[pointer] 
            
            # move pointer over
            pointer += key 
            
    # Convert the ciphertext list into a single string value and return it.
    return ''.join(ciphertext)  


def transposition_decryptMessage(key, message): 
    # The transposition decrypt function will simulate the "columns" and 
    # "rows" of the grid that the plaintext is written on by using a list 
    # of strings. First, we need to calculate a few values.
    
    # The number of "columns" in our transposition grid:
    numOfColumns = math.ceil(len(message) / key) 
    
    # The number of "rows" in our grid will need:
    numOfRows = key 
    
    # The number of "shaded boxes" in the last "column" of the grid: 
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message) 
    
    # Each string in plaintext represents a column in the grid.
    plaintext = [''] * numOfColumns 
    
    # The col and row variables point to where in the grid the next 
    # character in the encrypted message will go.
    col = 0 
    row = 0 
    
    for symbol in message: 
        plaintext[col] += symbol 
        col += 1 # point to next column 
        
        # If there are no more columns OR we're at a shaded box, go back to 
        # the first column and the next row. 
        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            col = 0 
            row += 1 
    
    return ''.join(plaintext) 
       

#--------------------------------

#-RSA (Python recipe) 
"""\
The author takes no responsibility for anything having anything to do
with this code. Use at your own risk, or don't use at all.

This is a Python implementation functions used in the RSA algorithm, as
well as a file-like object for writing encrypted files that it can later
read using the same password. This is useful for if you want store
sensitive data to a file with a user-given password.

The RSA keys are obtained as follows:
1. Choose two prime numbers p and q
2. Compute n=pq
3. Compute φ(n)=totient(p,q)
4. Choose e coprime to φ(n) such that gcd(e,n)=1
5. Compute d=modInverse(e,φ(n))
6. e is the publickey; n is also made public; d is the privatekey

Encryption is as follows:
1. Size of data to be encrypted must be less than n
2. ciphertext=pow(plaintext,publickey,n)

Decryption is as follows:
1. Size of data to be encrypted must be less than n
2. plaintext=pow(ciphertext,privatekey,n)
"""

import random,md5

def RabinMillerWitness(test,possible):
    #calculates (a**b)%n via binary exponentiation, yielding itermediate
    #results as Rabin-Miller requires
    #written by Josiah Carlson
    #modified and optimized by Collin Stocks
    a,b,n=long(test%possible),possible-1,possible
    if a==1:
        return False
    A=a
    t=1L
    while t<=b:
        t<<=1
    #t=2**k, and t>b
    t>>=2
    while t:
        A=pow(A,2,n)
        if t&b:
            A=(A*a)%n
        if A==1:
            return False
        t>>=1
    return True

smallprimes = (3,5,7,11,13,17,19,23,29,31,37,41,43,
                47,53,59,61,67,71,73,79,83,89,97)

def getPrime(b,seed):
    #Generates an integer of b bits that is probably prime
    #written by Josiah Carlson
    #modified (heavily) and optimized by Collin Stocks
    bits=int(b)
    assert 64<=bits
    k=bits<<1
    possible=seed|1 # make it odd
    good=0
    while not good:
        possible+=2 # keep it odd
        good=1
        for i in smallprimes:
            if possible%i==0:
                good=0
                break
        else:
            for i in xrange(k):
                test=random.randrange(2,possible)|1
                if RabinMillerWitness(test,possible):
                    good=0
                    break
    return possible

def egcd(a,b):
    # Extended Euclidean Algorithm
    # returns x, y, gcd(a,b) such that ax + by = gcd(a,b)
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

def gcd(a,b):
    # 2.8 times faster than egcd(a,b)[2]
    a,b=(b,a) if a<b else (a,b)
    while b:
        a,b=b,a%b
    return a

def modInverse(e,n):
    # d such that de = 1 (mod n)
    # e must be coprime to n
    # this is assumed to be true
    return egcd(e,n)[0]%n

def totient(p,q):
    # Calculates the totient of pq
    return (p-1)*(q-1)

def passwordToPrimePair(pswd,bits=64):
    assert 64<=bits
    assert bits%4==0
    length=bits//4
    sep=len(pswd)//2
    append="0"*(length-sep)
    seed1=int(pswd[:sep]+append,16)
    seed2=int(pswd[sep:]+append,16)
    p=getPrime(bits,seed1)
    q=getPrime(bits,seed2)
    return p,q

def passwordToKey(password,bits=64):
    assert 64<=bits
    assert bits%4==0
    length=bits//4
    pswd=md5.new(password).hexdigest()
    p,q=passwordToPrimePair(pswd,bits)
    n=p*q
    append="0"*(length-len(pswd))
    possible=int(pswd+append,16)|1 # n is always even
                            # so possible must be odd
    while not gcd(possible,n):
        possible+=2 # keep it odd
    private=possible
    public=modInverse(private,totient(p,q))
    return public,private,n

def rsa_crypt(string,power,n):
    data1=0L
    for char in string:
        data1<<=8
        data1+=ord(char)
    data2=pow(data1,power,n)
    ret=""
    while data2:
        data2,r=divmod(data2,256)
        ret=chr(r)+ret
    return ret

def encrypt(string,power,n,bits=128):
    string=string.replace('/',"/s").replace('\0',"/0") # escape \x00
                # because rsa_crypt() ignores leading zeros
    bytes=bits//8
    lst=[]
    while string:
        lst.append(string[:bytes-1]) # string must have a lesser value than
        string=string[bytes-1:] # n, so truncate and pad
    for i in range(len(lst)):
        lst[i]=rsa_crypt(lst[i],power,n)
        lst[i]='\0'*(bytes-len(lst[i]))+lst[i] # pad with zeros
            # don't worry about removing these later: crypt() ignores
            # leading zeros already, so they are always removed
    return ''.join(lst) # the length of this must be a multiple of bytes

def decrypt(string,power,n,bits=128):
    bytes=bits//8
    lst=[]
    while string:
        lst.append(string[:bytes])
        string=string[bytes:]
    for i in range(len(lst)):
        lst[i]=rsa_crypt(lst[i],power,n)
    ret=''.join(lst)
    ret=ret.replace("/0",'\0').replace("/s",'/')
    return ret

#            data=data.replace('/',"/s").replace('\0',"/0")
#            data=data.replace("/0",'\0').replace("/s",'/')

class secureFile(object):
    # Provides a file-like object for creating secure files that it can
    # later read. It takes a string as a password that it uses to generate
    # both prime numbers and the encryption key.
    def __init__(self,fileobj,password,bits=128,mode="rb"):
        # Function must be passed an open file or a file name,
        # and on operating systems where this matters, the
        # binary attribute must be set.
        # For example, open("file","rb"), not open("file","r")
        if type(fileobj)==str:
            fileobj=open(fileobj,mode)
        self.f=fileobj
        self.e,self.d,self.n=passwordToKey(password,bits//2)
        self.bits=bits
        self.rbuf=""
        self.wbuf=""
    def write(self,data):
        self.wbuf+=data
        e,n,bits,bytes=self.e,self.n,self.bits,self.bits//8
        while bytes<len(self.wbuf):
            self.f.write(rsa_crypt(self.data[:bytes],e,n,bits))
            self.wbuf=self.wbuf[bytes:]
    def flush(self):
        self.f.write(rsa_crypt(self.wbuf,self.e,self.n,self.bits))
        self.wbuf=""
    def read(self,bytes=None):
        if bytes==None:
            self.rbuf+=decrypt(self.f.read(),self.d,self.n,self.bits)
            ret=self.rbuf
            self.rbuf=""
        else:
            _bytes=bytes-len(self.rbuf)
            rbytes=_bytes+(self.bits-_bytes%self.bits)
            self.rbuf+=decrypt(self.f.read(rbytes),self.d,self.n,self.bits)
            ret=self.rbuf[:bytes]
            self.rbuf=self.rbuf[bytes:]
        return ret
    def readline(self):
        ret=""
        while not ret.endswith('\n'):
            ln=len(ret)
            ret+=self.read(1)
            if len(ret)==ln:
                break
        return ret
    def readlines(self):
        ret=[]
        while ret[-1]:
            ret.append(self.readline())
        return ret[:-1]
    def next(self):
        ret=self.readline()
        if len(ret)==0:
            raise StopIteration
    def __iter__(self):
        return self
    def close(self):
        self.flush()
        self.f.close()

try:
    import psyco
    psyco.bind(RabinMillerWitness)
    psyco.bind(getPrime)
    psyco.bind(egcd)
    psyco.bind(gcd)
    psyco.bind(modInverse)
    psyco.bind(totient)
    psyco.bind(passwordToPrimePair)
    psyco.bind(passwordToKey)
    psyco.bind(rsa_crypt)
    psyco.bind(encrypt)
    psyco.bind(decrypt)
    psyco.bind(secureFile)
except ImportError:
    pass
#--------------------------------