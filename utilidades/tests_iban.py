#!/usr/bin/env python3
#coding=utf-8

from utilidades.basedatos.CalculadorIBAN import CalculadorIBAN

import unittest

class TestIban(unittest.TestCase):
    
    def test_digito_control_correcto(self):
        #El digito de control de esto es 06
        cuenta="12345678061234567890"
        dc_calculado=CalculadorIBAN.get_digito_control(cuenta)
        self.assertEqual("06", dc_calculado)
    def test_digito_control_incorrecto(self):
        #El digito de control de esto es 06, sin embargo hemos puesto 90
        cuenta="12345678901234567890"
        dc_calculado=CalculadorIBAN.get_digito_control(cuenta)
        self.assertEqual("06", dc_calculado)
    def test_iban_1(self):
        cuenta="12345678061234567890"
        iban_calculado=CalculadorIBAN.get_iban(cuenta)
        self.assertEqual("ES68", iban_calculado)
    def test_iban_2(self):
        cuenta="00112233365566778899"
        iban_calculado=CalculadorIBAN.get_iban(cuenta)
        self.assertEqual("ES15", iban_calculado)
    def test_iban_con_espacios(self):
        cuenta="0011 2233 36 5566778899"
        iban_calculado=CalculadorIBAN.get_iban(cuenta)
        self.assertEqual("ES15", iban_calculado)
    def test_iban_con_guiones(self):
        cuenta="0011-2233-36-5566778899"
        iban_calculado=CalculadorIBAN.get_iban(cuenta)
        self.assertEqual("ES15", iban_calculado)
        
if __name__ == '__main__':
    unittest.main()