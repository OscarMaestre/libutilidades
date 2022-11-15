from random import choice, randint
import unittest


class Generator(object):
    CLASE_A="A"
    CLASE_B="B"
    CLASE_C="C"
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

    @staticmethod
    def convertir_mascara_cidr_a_binario(cantidad_bits):
        mascara_binaria=("1"*cantidad_bits)+("0"*(32-cantidad_bits))
        return mascara_binaria

    @staticmethod
    def convertir_mascara_cidr_a_decimal(cantidad_bits):
        secuencia_binaria=Generator.convertir_mascara_cidr_a_binario(cantidad_bits)
        mascara_con_puntos=Generator.convertir_binario_a_ip(secuencia_binaria)
        return mascara_con_puntos

    @staticmethod 
    def generar_direccion_de_red_de_clase_a():
        #Generamos 31 bits al azar y ponemos como primer bit el 0
        secuencia=Generator.generar_secuencia_binaria(31)
        secuencia="0"+secuencia
        bits_mascara=randint(6, 27)
        return (secuencia, bits_mascara, Generator.CLASE_A)
    
    @staticmethod 
    def generar_direccion_de_red_de_clase_b():
        #Generamos 30 bits al azar y ponemos como primeros bits "10"
        secuencia=Generator.generar_secuencia_binaria(30)
        secuencia="10"+secuencia
        bits_mascara=randint(16, 27)
        return (secuencia, bits_mascara, Generator.CLASE_B)

    @staticmethod 
    def generar_direccion_de_red_de_clase_c():
        #Generamos 29 bits al azar y ponemos como primeros bits "110"
        secuencia=Generator.generar_secuencia_binaria(30)
        secuencia="110"+secuencia
        bits_mascara=randint(24, 28)
        return (secuencia, bits_mascara, Generator.CLASE_C)

class Tests(unittest.TestCase):
    def test_secuencia_binaria(self):
        longitud=24
        secuencia=Generator.generar_secuencia_binaria(longitud)
        self.assertEqual(longitud, len(secuencia))
        #print(secuencia)
    def test_binario1(self):
        longitud=32
        secuencia=Generator.generar_secuencia_binaria(longitud)
        direccion_ip=Generator.convertir_binario_a_ip(secuencia)
        #print(direccion_ip)
    def test_de_binario_a_ip(self):
        longitud=32
        secuencia=Generator.generar_secuencia_binaria(longitud)
        direccion_ip=Generator.convertir_binario_a_ip(secuencia)
        nueva_secuencia=Generator.convertir_ip_a_binario(direccion_ip, con_puntos=False)
        self.assertEqual(secuencia, nueva_secuencia)
    def test_generacion_clase_a(self):
        (direccion_clase_a, bits_red)=Generator.generar_direccion_de_red_de_clase_a()
        direccion_clase_a=Generator.convertir_binario_a_ip(direccion_clase_a)
        cadena="{0}/{1}".format(direccion_clase_a, bits_red)
        #print(cadena)
    def test_generacion_clase_b(self):
        (direccion_clase_b, bits_red)=Generator.generar_direccion_de_red_de_clase_b()
        direccion_clase_b=Generator.convertir_binario_a_ip(direccion_clase_b)
        cadena="{0}/{1}".format(direccion_clase_b, bits_red)
        #print(cadena)
    def test_generacion_clase_c(self):
        (direccion_clase_c, bits_red)=Generator.generar_direccion_de_red_de_clase_b()
        direccion_clase_c=Generator.convertir_binario_a_ip(direccion_clase_c)
        cadena="{0}/{1}".format(direccion_clase_c, bits_red)
        #print(cadena)
    def test_convertir_cidr_a_binario(self):
        secuencia="1"*32
        bits=32
        secuencia_convertida=Generator.convertir_mascara_cidr_a_binario(bits)
        self.assertEqual(secuencia, secuencia_convertida)

        secuencia="1"*30+"00"
        bits=30
        secuencia_convertida=Generator.convertir_mascara_cidr_a_binario(bits)
        self.assertEqual(secuencia, secuencia_convertida)

        secuencia="1"*20+"0"*12
        bits=20
        secuencia_convertida=Generator.convertir_mascara_cidr_a_binario(bits)
        self.assertEqual(secuencia, secuencia_convertida)
        
    def test_convertir_mascara_a_decimal(self):
        mascara_calculada=Generator.convertir_mascara_cidr_a_decimal(32)
        mascara_esperada="255.255.255.255"
        self.assertEqual(mascara_calculada, mascara_esperada)

        mascara_calculada=Generator.convertir_mascara_cidr_a_decimal(24)
        mascara_esperada="255.255.255.0"
        self.assertEqual(mascara_calculada, mascara_esperada)

        mascara_calculada=Generator.convertir_mascara_cidr_a_decimal(16)
        mascara_esperada="255.255.0.0"
        self.assertEqual(mascara_calculada, mascara_esperada)

        mascara_calculada=Generator.convertir_mascara_cidr_a_decimal(18)
        mascara_esperada="255.255.192.0"
        self.assertEqual(mascara_calculada, mascara_esperada)

        
        
        

if __name__=="__main__":
    unittest.main()
