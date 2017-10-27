#!/usr/bin/env python3

import platform
import sys, os
import unittest

from GestorExcel import EscritorExcel

RUTA_ESTE_FICHERO=(os.path.abspath(__file__))
NOMBRE_SISTEMA_OPERATIVO=platform.system()

if NOMBRE_SISTEMA_OPERATIVO=="Linux":
    FICHERO_EJEMPLO=(".." + os.sep ) * 6
    FICHERO_EJEMPLO+="hoja_ejemplo.xls"
else:
    print ("No hay una hoja de calculo definida en el fichero {0}".format( RUTA_ESTE_FICHERO ))
    sys.exit(-1)
    
class TestClaseExcel(unittest.TestCase):
    def setUp(self):
        self.fichero_excel=None
    def test_carga(self):
        self.fichero_excel=EscritorExcel("archivo_ejemplo.xls")
        self.fichero_excel.anadir_hoja("Afiliados_Importacion")
        self.fichero_excel.escribir_en_hoja(4, 0, "aaa")
        self.fichero_excel.guardar()
    def test_defecto(self):
        self.fichero_excel=EscritorExcel()
        self.fichero_excel.set_configuracion_tipica()
        self.fichero_excel.escribir_en_hoja(4, 0, "aaa")
        self.fichero_excel.guardar()
    
if __name__ == '__main__':
    unittest.main()