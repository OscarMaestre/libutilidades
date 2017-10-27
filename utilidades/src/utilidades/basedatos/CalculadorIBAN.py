#!/usr/bin/env python3
#coding=utf-8

class CalculadorIBAN(object):
    @staticmethod
    def get_entero_posicion(texto, pos):
        return int ( texto[pos] )
    
    @staticmethod
    def get_digito_control(texto):
        #print (texto)
        primera_cifra_codigo_banco      =       CalculadorIBAN.get_entero_posicion(texto, 0)
        segunda_cifra_codigo_banco      =       CalculadorIBAN.get_entero_posicion(texto, 1)
        tercera_cifra_codigo_banco      =       CalculadorIBAN.get_entero_posicion(texto, 2)
        cuarta_cifra_codigo_banco       =       CalculadorIBAN.get_entero_posicion(texto, 3)
        
        primera_cifra_codigo_entidad    =       CalculadorIBAN.get_entero_posicion(texto, 4)
        segunda_cifra_codigo_entidad    =       CalculadorIBAN.get_entero_posicion(texto, 5)
        tercera_cifra_codigo_entidad    =       CalculadorIBAN.get_entero_posicion(texto, 6)
        cuarta_cifra_codigo_entidad     =       CalculadorIBAN.get_entero_posicion(texto, 7)
        
        suma_primer_digito_control = \
            ( 4 * primera_cifra_codigo_banco )   + ( 8   * segunda_cifra_codigo_banco ) + \
            ( 5 * tercera_cifra_codigo_banco )      + ( 10  * cuarta_cifra_codigo_banco ) + \
            ( 9 * primera_cifra_codigo_entidad )    + ( 7   * segunda_cifra_codigo_entidad )+ \
            ( 3 * tercera_cifra_codigo_entidad )    + ( 6   * cuarta_cifra_codigo_entidad )
            
        resto_primer_digito_control = suma_primer_digito_control % 11
        
        
        primer_digito_de_control = 11 - resto_primer_digito_control
        if (primer_digito_de_control==11) :
            primer_digito_de_control=0
        
        if (primer_digito_de_control==10) :
            primer_digito_de_control=1
        
        
        multiplicadores_segundo_digito=[1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
        suma_segundo_digito_control=0
        
        for i in range(0, 10) :
            suma_segundo_digito_control += CalculadorIBAN.get_entero_posicion(texto, 10+i) * multiplicadores_segundo_digito[i]
        
            
        resto_segundo_digito_control = suma_segundo_digito_control % 11
        
        
        segundo_digito_de_control = 11 - resto_segundo_digito_control
        if (segundo_digito_de_control==11) :
            segundo_digito_de_control=0
        
        if (segundo_digito_de_control==10) :
            segundo_digito_de_control=1
        return str(primer_digito_de_control) + str(segundo_digito_de_control)
    
    @staticmethod
    def get_iban(texto):
        elementos_a_quitar=["-", " "]
        for elemento in elementos_a_quitar:
            texto=texto.replace ( elemento, "")
        
        cadena_para_calcular_iban=texto+"14"+"28"+"00"
        numeroGrande=int(cadena_para_calcular_iban)
        resto=numeroGrande % 97
        diferencia=98 - resto
        if (diferencia<10) :
            diferencia="0"+str(diferencia)
        else:
            diferencia=str(diferencia)
        
        return "ES"+diferencia
    
