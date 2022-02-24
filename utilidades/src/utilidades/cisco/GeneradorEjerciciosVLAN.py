#!/usr/bin/python3
 

from utilidades.ip.ipv4 import GeneradorIPV4Azar
from utilidades.cisco.CiscoIOS import CiscoIOS
from string import Template
from random import choice, shuffle, seed, randint


class GeneradorEjerciciosVLAN(object):
    def __init__(self) -> None:
        self.enunciados=[]
        self.switch=CiscoIOS()
        self.identificadores_vlan=[str(10*x) for x in range(1, 20)]
        self.nombres_vlan=[
            "CONTABILIDAD", "GESTION", "DIRECCION", "GERENCIA",
            "TECNICOS", "DISENO", "PROGRAMADORES", "ANALISIS",
            "FINANZAS", "ADMINS", "USUARIOS01", "USUARIOS02",
            "USUARIOS03", "CLIENTES", 
        ]
        self.dominios_vtp=[
            "aulab14.com", "aulab15.com", "aulab09.com",
            "acme.com", "tecsa.com", "iesmaestre.com",
            "maestre.es"
        ]
        self.claves_vtp=[
            "vtpadmin", "admin1234vtp", "admin_1234vtp", "vtp1234admin",
            "administradorvtp", "vtpadministrador_1234"
        ]
        self.puertos=[x for x in range(1, 17)]
        self.vlan_vtp=["VLANINTERNO", "VLANGESTION", "VLANVTP", "VTP"]

    def get_idvlan_al_azar(self):
        return choice(self.identificadores_vlan)

    def get_nombre_vlan_azar(self):
        return choice (self.nombres_vlan)

    def get_tuplas_vlans(self, cantidad_vlans):
        shuffle(self.nombres_vlan)
        shuffle(self.identificadores_vlan)
        return list(zip(
            self.identificadores_vlan[0:cantidad_vlans],
            self.nombres_vlan[0:cantidad_vlans]))

    def get_tuplas_puertos_vlans(self, cantidad_vlans):
        shuffle(self.puertos)
        shuffle(self.identificadores_vlan)
        return list(zip(
            self.nombres_vlan[0:cantidad_vlans],
            self.identificadores_vlan[0:cantidad_vlans]))

    def crear_vlans(self):
        cantidad_vlans=randint(3,7)
        vlans=self.get_tuplas_vlans(cantidad_vlans)
        lista_para_enunciado=[tupla[1]+" con ID "+str(tupla[0]) for tupla in vlans]
        texto_lista_vlans=", ".join(lista_para_enunciado)
        enunciado="Crear estas VLANs con exactamente estos identificadores y estos nombres:"+texto_lista_vlans
        for tupla in vlans:
            id_vlan=str(tupla[0])
            nombre_vlan=tupla[1]
            self.switch.crear_vlan(id_vlan, nombre_vlan)
        return enunciado

    def get_comandos_con_prompt(self):
        return self.switch.get_comandos_con_prompt()
    
    def get_comandos_sin_prompt(self):
        return self.switch.get_comandos_sin_prompt()

    def poner_puerto_en_acceso_vlan(self, num_puerto, id_vlan):
        self.switch.poner_interfaz_acceso(num_puerto, id_vlan)

    def asignar_puertos(self):
        shuffle(self.puertos)
        shuffle(self.identificadores_vlan)
        #Unos cuantos puertos se pondrán en modo acceso y algunos
        #en modo troncal
        num_puertos_acceso=randint(4,6)
        num_puertos_troncales=randint(2,3)
        puertos_acceso=self.puertos[0:num_puertos_acceso]
        puertos_troncales=self.puertos[num_puertos_acceso+1:num_puertos_acceso+1+num_puertos_troncales]
        vlans=self.identificadores_vlan[0:num_puertos_acceso]
        vlans_troncales=self.identificadores_vlan[num_puertos_acceso+1:num_puertos_acceso+1+num_puertos_troncales]

        asignaciones_acceso=list(zip(puertos_acceso, vlans))
        cadenas_acceso=["interfaz FastEthernet 0/{0} a VLAN {1}".format(tupla[0], tupla[1]) for tupla in asignaciones_acceso]
        texto_acceso="Poner estas interfaces en modo acceso asignándolas a estas VLAN:"+",".join(cadenas_acceso)
        for tupla in asignaciones_acceso:
            self.switch.poner_interfaz_acceso(tupla[0], tupla[1])

        
        asignaciones_troncales=list(zip(puertos_troncales, vlans_troncales))
        cadenas_troncales=["interfaz FastEthernet 0/{0} a VLAN {1}".format(tupla[0], tupla[1]) for tupla in asignaciones_troncales]
        texto_troncal="Poner estas interfaces en modo acceso asignándolas a estas VLAN:"+",".join(cadenas_troncales)

        for tupla in asignaciones_troncales:
            self.switch.poner_interfaz_troncal(tupla[0], tupla[1])
        return texto_acceso+"."+texto_troncal
        
    def poner_vtp_transparente(self):
        enunciado="Poner el switch en modo VTP transparente."
        self.switch.vtp_transparent()
        return enunciado

    def poner_vtp_servidor(self):
        dominio=choice(self.dominios_vtp)
        clave=choice(self.claves_vtp)
        enunciado="Poner el switch en modo servidor dentro del dominio {0} y poniendo la clave {1}".format(dominio, clave)
        self.switch.poner_vtp_modo_servidor(dominio, clave)
        return enunciado

    def poner_vtp_cliente(self):
        dominio=choice(self.dominios_vtp)
        clave=choice(self.claves_vtp)
        enunciado="Poner el switch en modo cliente dentro del dominio {0} y poniendo la clave {1}".format(dominio, clave)
        self.switch.poner_vtp_modo_cliente(dominio, clave)
        return enunciado
    
    def elegir_modo_vtp(self):
        metodo=choice(
            [self.poner_vtp_cliente, self.poner_vtp_servidor, self.poner_vtp_transparente]
        )
        return metodo()

    def mostrar_vlans(self):
        enunciado="Mostrar las VLANs"
        self.switch.mostrar_vlans()
        return enunciado
    
    def generar_ejercicio(self):
        metodos=[
            self.elegir_modo_vtp, self.asignar_puertos, self.crear_vlans, self.mostrar_vlans
        ]
        shuffle(metodos)

        for metodo in metodos:
            enunciado=metodo()
            self.enunciados.append(enunciado)
    
    def get_enunciado(self):
        enunciado="Configurar un switch Cisco mediante la línea de comandos cumpliendo los requisitos siguientes:\n\n"
        conpuntos=["* "+punto for punto in self.enunciados]
        return enunciado + "\n".join(conpuntos)

    def get_solucion(self):
        texto=self.get_enunciado()+"\n\n"
        texto+="La solución detallada sería esta::\n\n"
        con_prompt=["\t"+comando for comando in self.switch.comandos_con_prompt]
        texto+="\n".join(con_prompt)

        texto+="\n\nLos comandos listos para copiar y pegar serían estos::\n\n"
        sin_prompt=["\t"+comando for comando in self.switch.comandos_sin_prompt]
        texto+="\n".join(sin_prompt)
        return texto