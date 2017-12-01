#!/usr/bin/env python3
#coding=utf-8

from utilidades.ficheros.GestorFicheros import GestorFicheros

import unittest

class TestFichero(unittest.TestCase):
    
    def get_cantidad_lineas_fichero(self, nombre):
        with open(nombre, "r") as fich:
            lineas=fich.readlines()
            cantidad_lineas=len(lineas)
        return cantidad_lineas
    
    def test_cuenta_lineas(self):
        gf=GestorFicheros()
        ficheros=["fichero_ejemplo1.txt", "fichero_ejemplo2.txt", "fichero_ejemplo3.txt"]
        for f in ficheros:
            num_lineas_segun_gf     =   gf.CountLines(f)
            num_lineas_segun_python =   self.get_cantidad_lineas_fichero(f)
            self.assertEqual(num_lineas_segun_python, num_lineas_segun_gf)
            
if __name__ == '__main__':
    unittest.main()