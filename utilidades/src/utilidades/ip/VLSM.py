from dataclasses import dataclass

from ipaddress import IPv4Network, ip_network
from math import log2, ceil

from numpy import diff

@dataclass
class SolucionVLSM(object):
    nueva_red:IPv4Network
    def get_rst(self):
        hosts=list(self.nueva_red.hosts())
        ip_red=self.nueva_red
        
        primera_ip=hosts[0]
        ultima_ip=hosts[-1]
        ip_binaria=ultima_ip.packed
        ip_broadcast=self.nueva_red.broadcast_address
        definiciones=["IP de Red", "Primera IP", "Última IP", "IP de broadcast"]
        valores=[ip_red, primera_ip, ultima_ip, ip_broadcast]
        lista=[]
        for d,v in zip(definiciones, valores):
            lista.append("* {0}: {1}".format(d, v))
        return "\n".join(lista)

class VLSM(object):
    def __init__(self, lista_numeros_hosts, ipv4) -> None:
        self.lista_numeros_hosts=lista_numeros_hosts
        self.ip_de_red=ipv4
        self.soluciones=self.resolver()

    def get_bits_necesarios_para_cantidad_hosts(self, cantidad_hosts):
        #print("Bits para:"+str(cantidad_hosts))
        num_bits=ceil(log2(cantidad_hosts))
        return num_bits

    def get_nueva_direccion_de_red(self, ip_red_anterior, nueva_longitud_prefijo_red):
        aviso="\tIP anterior recibida {0}, nueva_longitud {1}".format(ip_red_anterior, nueva_longitud_prefijo_red)
        print(aviso)
        ultimo_host=ip_red_anterior.broadcast_address
        print("\tUltimo host:"+str(ultimo_host))
        ultimo_host_como_entero=int(ultimo_host)
        siguiente_ip_como_entero=ultimo_host_como_entero+1
        tupla=(siguiente_ip_como_entero, nueva_longitud_prefijo_red)
        siguiente_ip_como_red=IPv4Network(tupla)
        print("\tDevolvemos nueva IP  de red:"+str(siguiente_ip_como_red))
        return siguiente_ip_como_red

    def generar_red(self, ip_red, nuevos_bits_de_red):
        trozos=str(ip_red).split("/")
        print(trozos)
        direccion_nueva="{0}/{1}".format(trozos[0], nuevos_bits_de_red)
        nueva_ip=IPv4Network(direccion_nueva)
        print("La nueva IP es:"+str(nueva_ip))
        return nueva_ip

    def resolver(self):
        redes_solucion=[]
        lista_ordenada=sorted(self.lista_numeros_hosts, reverse=True)
        #print("Lista ordenada"+str(lista_ordenada))
        bits_de_host=self.get_bits_necesarios_para_cantidad_hosts(lista_ordenada[0])
        ip_red_anterior=self.ip_de_red
        print(ip_red_anterior)
        #print("Numbits:"+str(bits_de_host))
        for numero in lista_ordenada:
            nuevos_bits_de_host=self.get_bits_necesarios_para_cantidad_hosts(numero)
            if nuevos_bits_de_host<bits_de_host:
                print("Los bits de host {0} cambian a {1}".format(bits_de_host, nuevos_bits_de_host))
                bits_de_host=nuevos_bits_de_host
            nuevos_bits_de_red=32-bits_de_host  
            print("Nuevos bits de red:"+str(nuevos_bits_de_red))  
            
            
            ip_red_anterior=self.get_nueva_direccion_de_red(ip_red_anterior, nuevos_bits_de_red)
            redes_solucion.append(SolucionVLSM(ip_red_anterior))
            print("La nueva red anterior es:"+str(ip_red_anterior))
            
        return redes_solucion

if __name__=="__main__":
    ip=IPv4Network("10.0.0.0/18")
    print("Longitud prefijo:"+str(ip.prefixlen))
    hosts=[45, 29, 14, 3]
    vlsm=VLSM(hosts, ip)
    for s in vlsm.soluciones:
        print(s.get_rst())
        print()