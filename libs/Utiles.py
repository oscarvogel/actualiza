# coding=utf-8
# encoding: utf-8
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Utilidades varias necesarias en el sistema
import logging
import os
import sys
import traceback
from functools import wraps

import win32api
from configparser import ConfigParser
from sys import argv

from PyQt5 import QtGui
from os.path import join


def LeerIni(clave=None, key=None):
    retorno = ''
    Config = ConfigParser()
    Config.read("sistema.ini")
    try:
        if not key:
            key = 'param'
        retorno = Config.get(key, clave)
    except:
        # Ventanas.showAlert("Sistema", "No existe la seccion {}".format(clave))
        print("No existe la seccion {}".format(clave))

    return retorno


def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"), "a", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def icono_sistema():

    cIcono = QtGui.QIcon(imagen("logo.png"))
    return cIcono

def imagen(archivo):
    archivoImg = ubicacion_sistema() + join("imagenes", archivo)

    if os.path.exists(archivoImg):
        return archivoImg
    else:
        return ""

def ubicacion_sistema():
    cUbicacion = LeerIni("iniciosistema") #or os.path.dirname(argv[0])

    return cUbicacion

def DeCodifica(dato):
    # return "{}".format(bytearray(dato, 'latin-1', errors='ignore').decode('utf-8','ignore'))
    # return '{}'.format(bytearray(str(dato))).decode('utf-8').encode('latin-1')
    return "{}".format(bytearray(dato, 'latin-1', errors='ignore').decode('utf-8','ignore'))


def validar_cuit(cuit):
    # validaciones minimas
    if len(cuit) != 13 or cuit[2] != "-" or cuit[11] != "-":
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    cuit = cuit.replace("-", "") # remuevo las barras

    # calculo el digito verificador:
    aux = 0
    for i in range(10):
        aux += int(cuit[i])* base[i]

    aux = 11 - (aux - (int(aux / 11)* 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])

#==============================================================================
def getFileProperties(fname):
#==============================================================================
    """
    Read all properties of the given file return them as a dictionary.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        pass

    return props

def inicializar_y_capturar_excepciones(func):
    "Decorador para inicializar y capturar errores"
    @wraps(func)
    def capturar_errores_wrapper(self, *args, **kwargs):
        try:
            # inicializo (limpio variables)
            self.Traceback = self.Excepcion = ""
            return func(self, *args, **kwargs)
        except Exception as e:
            ex = traceback.format_exception( sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
            self.Traceback = ''.join(ex)
            self.Excepcion = traceback.format_exception_only( sys.exc_info()[0], sys.exc_info()[1])[0]
            logging.debug(self.Traceback)
            #Ventanas.showAlert("Error", "Se ha producido un error \n{}".format(self.Excepcion))
            if self.LanzarExcepciones:
                raise
        finally:
            pass
    return capturar_errores_wrapper
