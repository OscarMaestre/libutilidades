#!/usr/bin/env python3
#coding=utf-8

from utilidades.basedatos.CalculadorLetraDNI import CalculadorLetraDNI

import unittest

class TestDNI(unittest.TestCase):
    
    def test_dni_correcto_1(self):
        dni="05535031"
        letra=CalculadorLetraDNI.get_letra(dni)
        self.assertEqual("N", letra)
    def test_dni_correcto_2(self):
        dni="039830284"
        letra=CalculadorLetraDNI.get_letra(dni)
        self.assertEqual("B", letra)
        
    def test_dni_correcto_3(self):
        dni="39830284"
        letra=CalculadorLetraDNI.get_letra(dni)
        self.assertEqual("B", letra)


if __name__ == '__main__':
    unittest.main()