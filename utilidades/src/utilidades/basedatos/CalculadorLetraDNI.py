#!/usr/bin/env python3
#coding=utf-8

class CalculadorLetraDNI(object):
    @staticmethod
    def get_letra(dni):
        modulo=(int (dni)) %23
        letras_dni="TRWAGMYFPDXBNJZSQVHLCKE"
        return letras_dni[modulo]
