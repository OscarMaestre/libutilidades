from random import randint, random, seed, choice
from dataclasses import dataclass
import ipaddress

class GeneradorIPV4Azar(object):

    def __init__(self, num_ejercicio, cantidad_bits_mascara=None) -> None:
        """Constructor
        
            Argumentos:
            
                :param num_ejercicio: Número de ejercicio con el que aparecerá 
                
                :param cantidad_bits_mascara: Cantidad de bits a 1 en la máscara"""
        self.primer_byte=randint(8, 52)
        if cantidad_bits_mascara!=None:
            self.bits_mascara=cantidad_bits_mascara
        else:
            self.bits_mascara=randint(10, 28)
        #print("Mascara:/"+str(self.bits_mascara))
        self.bits_host=32-self.bits_mascara
        self.secuencia_binaria=self.generar()
        
        self.cadena=self.convertir_a_decimal(self.secuencia_binaria)
        #print(self.cadena)
        self.direccion=ipaddress.IPv4Network(
            self.cadena+"/"+str(self.bits_mascara)
        )
        self.todos_hosts=list(self.direccion.hosts())
        self.mascara_en_decimal=self.get_mascara_en_decimal()
        self.num_ejercicio=num_ejercicio

    def convertir_a_decimal(self, secuencia_binaria):
        """Dada una secuencia en binario de 32 bits nos devuelve
        la dirección en decimal.
    
        
            :param secuencia_binaria: secuencia de 32 bits"""
        bytes_ip=[]
        for i in range(0, 4):
            li=i*8
            ls=li+8
            trozo=int(secuencia_binaria[li:ls], 2)
            bytes_ip.append(str(trozo))
        cadena=".".join(bytes_ip)
        return cadena

    def get_direccion_en_binario(self, direccion):
        """Dada una dirección en decimal como 192.168.1.39/24
        nos devuelve el equivalente en binario
        
            :param direccion:  Dirección en decimal como 192.168.1.39/24"""
        trozos=str(direccion).split("/")
        binario='{:#b}'.format(ipaddress.IPv4Address(trozos[0]))
        binario=binario[2:]
        bytes=[
            binario[0:8],
            binario[8:16],
            binario[16:24],
            binario[24:32]
        ]
        resultado=".".join(bytes)
        return resultado
    def get_mascara_en_decimal(self):
        """Devuelve la máscara de la dirección actual en decimal"""
        prefijo="1"*self.bits_mascara
        sufijo ="0"*self.bits_host
        mascara=prefijo+sufijo
        return self.convertir_a_decimal(mascara)
    def get_todos_hosts(self):
        """Devuelve una lista con todos los host de la red generada

                :returns hosts[]: una lista con todos los host
        
        """
    def get_ip_host(self, num_host=0):
        """Genera una IP válida de host:
        
            
                :param num_host:  Número de host (se extrae la IP número X del vector total de IPs
            

                :returns (ip, mascara):  Tupla con una IP y una máscara, todo en strings
        """
        ip_host=str(self.todos_hosts[num_host])
        return (ip_host, self.mascara_en_decimal)
        
    def generar(self):
        """Genera una dirección IP de red (no de host) al azar"""
        posibles_generadores=[]
        bits_host="0"*self.bits_host
        if self.bits_mascara>=24:
            posibles_generadores=[
                self.generar_clase_a, self.generar_clase_b,self.generar_clase_c]
            generador=choice(posibles_generadores)
            return generador(self.bits_mascara)+bits_host
        if self.bits_mascara>=16:
            posibles_generadores=[
                self.generar_clase_a, self.generar_clase_b]
            generador=choice(posibles_generadores)
            return generador(self.bits_mascara)+bits_host
        if self.bits_mascara>=8:
            posibles_generadores=[
                self.generar_clase_a]
            generador=choice(posibles_generadores)
            return generador(self.bits_mascara)+bits_host
            
    def generar_clase_a(self, num_bits):
        """Genera una dirección de clase A en la que haya
        tantos bits de red como se nos pida.
    
                :param num_bits: número de bits de red
        """
        return "0"+self.get_secuencia_azar_bits(num_bits-1)
    def generar_clase_b(self, num_bits):
        """Genera una dirección de clase B en la que haya
        tantos bits de red como se nos pida.
    
                :param num_bits: número de bits de red
        """
        return "10"+self.get_secuencia_azar_bits(num_bits-2)
    def generar_clase_c(self, num_bits):
        """Genera una dirección de clase C en la que haya
        tantos bits de red como se nos pida.
    
            :param num_bits: número de bits de red
        """
        return "110"+self.get_secuencia_azar_bits(num_bits-3)
    
    def get_bit(self):
        return choice(["0", "1"])

    def get_secuencia_azar_bits(self, num_bits):
        cadena=""
        for i in range(0, num_bits):
            cadena=cadena+self.get_bit()
        return cadena   
 