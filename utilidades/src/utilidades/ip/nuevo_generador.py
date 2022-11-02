from random import choice
import unittest


class Generador(object):
    @staticmethod
    def generar_secuencia_binaria(longitud_bits):
        bits=["0", "1"]
        secuencia=""
        for i in range(0, longitud_bits):
            secuencia=secuencia+choice(bits)
        return secuencia
    @staticmethod
    def convertir_ip_a_binario(ip, con_puntos=True):
        if con_puntos:
            separador="."
        else:
            separador=""

        cadena= separador.join([bin(int(x)+256)[3:] for x in ip.split('.')])
        return cadena

    @staticmethod
    def convertir_binario_a_ip(binario):
        bloques = [binario[0:8], binario[8:16], binario[16:24], binario[24:32]]
        
        secuencia=[]
    
        for bloque in bloques:
            #print("Bloque:"+bloque)
            secuencia.append(str(int(bloque, 2)))
        ip=".".join(secuencia)
        return ip

class Tests(unittest.TestCase):
    def test_secuencia_binaria(self):
        longitud=24
        secuencia=Generador.generar_secuencia_binaria(longitud)
        self.assertEqual(longitud, len(secuencia))
        #print(secuencia)
    def test_binario1(self):
        longitud=32
        secuencia=Generador.generar_secuencia_binaria(longitud)
        direccion_ip=Generador.convertir_binario_a_ip(secuencia)
        #print(direccion_ip)
    def test_de_binario_a_ip(self):
        longitud=32
        secuencia=Generador.generar_secuencia_binaria(longitud)
        direccion_ip=Generador.convertir_binario_a_ip(secuencia)
        nueva_secuencia=Generador.convertir_ip_a_binario(direccion_ip, con_puntos=False)
        self.assertEqual(secuencia, nueva_secuencia)

if __name__=="__main__":
    unittest.main()
