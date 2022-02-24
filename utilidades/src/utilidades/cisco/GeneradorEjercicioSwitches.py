#!/usr/bin/python3
 

from utilidades.ip.ipv4 import GeneradorIPV4Azar
from utilidades.cisco.CiscoIOS import CiscoIOS
from string import Template
from random import choice, shuffle, seed, randint


class GeneradorEjercicioSwitches(object):
    def __init__(self) -> None:
        self.enunciados=[]
        self.ejercicio=CiscoIOS()

    
    def get_clave_admin_azar(self):
        claves=[
            "admin", "admin1234", "admin_1234", "1234admin",
            "administrador", "administrador_1234"
        ]
        return choice(claves)

    def get_clave_telnet_azar(self):
        claves=[
            "admin", "admin1234", "admin_1234", "1234admin",
            "administrador", "administrador_1234"
        ]
        return choice(claves)
    
    def get_dominio_azar (self):
        dominios=[
            "acme.com", "empresa.com", "redes.es",
            "network.es", "academy.com", "redes.com"
        ]
        return choice(dominios)
    
    def get_longitud_clave_azar(self):
        longitudes=["512", "1024", "2048"]
        return choice(longitudes)

    def get_login_ssh_azar(self):
        logins=[
            "adminssh", "sshadmin", "administradorssh",
            "adminseguro", "adminporssh", "sshadministrador"
        ]
        return choice(logins)
    
    def get_nombres_switch_azar(self):
        nombres=[
            "AulaB08","AulaB09","AulaB10",
            "SwitchB08","SwitchB09","SwitchB10",
            "AulaB11","AulaB14","AulaB15",
            "SwitchB11","SwitchB14","SwitchB15"
        ]
        return choice(nombres)
    
    def get_clave_ssh_azar(self):
        return self.get_login_ssh_azar()

    def poner_clave_admin(self):
        plantilla="Poner al switch la clave de administrador ``{0}``."
        clave_admin_azar=self.get_clave_admin_azar()
        self.enunciados.append(plantilla.format(clave_admin_azar))
        self.ejercicio.poner_clave_admin(clave_admin_azar)
    
    def poner_clave_telnet(self):
        plantilla="Habilitar telnet y ponerle a este acceso la clave ``{0}``."
        clave_telnet_azar=self.get_clave_telnet_azar()
        self.enunciados.append(plantilla.format(clave_telnet_azar))
        self.ejercicio.poner_clave_telnet(clave_telnet_azar)

    def configurar_ssh(self):
        plantilla="Genera la pareja de claves para el dominio ``{0}`` con una longitud de clave de ``{1}``. Añade también un usuario ssh con en login ``{2}`` y la clave ``{3}``."
        dominio=self.get_dominio_azar()
        longitud=self.get_longitud_clave_azar()
        usuario_ssh=self.get_login_ssh_azar()
        clave_ssh=self.get_clave_ssh_azar()
        self.enunciados.append(plantilla.format(dominio, longitud, usuario_ssh, clave_ssh))
        self.ejercicio.generar_claves_publicas(dominio, longitud)
        self.ejercicio.configurar_usuario_ssh(usuario_ssh, clave_ssh)

    def poner_hostname(self):
        nombre=self.get_nombres_switch_azar()
        plantilla="Poner al switch el nombre ``{0}``."
        self.enunciados.append(plantilla.format(nombre))
        self.ejercicio.hostname(nombre)

    def poner_ip_azar(self):
        generador=GeneradorIPV4Azar(num_ejercicio=1)
        (direccion, mascara)=generador.get_ip_host()
        
        plantilla="Poner la IP ``{0}`` con la máscara ``{1}``. Recordar activar la interfaz VLAN."
        self.enunciados.append(plantilla.format(direccion, mascara))
        self.ejercicio.poner_ip_gestion(direccion, mascara)
        
    def poner_clave_consola_azar_con_login(self):
        claves=[
            "consola1234", "c0n50l4", "claveabcd",
            "consola33", "claveconsola1234","consola",
            "abcdefg"
        ]
        clave_azar=choice(claves)
        plantilla="Proteger el acceso por consola con la clave ``{0}`` asegurando que se exige el uso de dicha clave"
        self.enunciados.append(plantilla.format(clave_azar))
        self.ejercicio.poner_clave_consola_con_login(clave_azar)
    
    def poner_clave_consola_azar_sin_login(self):
        claves=[
            "consola1234", "claveclave", "claveabcd",
            "consola33", "claveconsola1234","consola",
            "abcdefg"
        ]
        clave_azar=choice(claves)
        plantilla="Proteger el acceso por consola con la clave ``{0}`` y no pidas por ahora el uso de dicha clave"
        self.enunciados.append(plantilla.format(clave_azar))
        self.ejercicio.poner_clave_consola_sin_login(clave_azar)
    

    def anadir_clave_mac_azar(self):
        mac_azar=self.ejercicio.generar_mac_azar()
        puerto_azar=choice([0,1,2,3,4,5,6,7,8])
        plantilla="Usando ARP estático asigna la MAC ``{0}`` al puerto ``FastEthernet 0/{1}``"
        self.enunciados.append(plantilla.format(mac_azar, puerto_azar))
        self.ejercicio.anadir_mac_puerto(mac_azar, puerto_azar)

    def cambiar_timeout(self):
        timeouts=[60, 120, 240, 600, 1200, 3600, 7200]
        plantilla="Modificar el timeout de ARP haciendo que tome un valor de {0} segundos."
        timeout_azar=choice(timeouts)
        self.enunciados.append(plantilla.format(timeout_azar))
        self.ejercicio.cambiar_timeout_arp(timeout_azar)
    
    def mostrar_la_tabla_de_macs(self):
        self.enunciados.append("Mostrar la tabla de MACS.")
        self.ejercicio.ver_tabla_macs()

    def guardar_la_configuracion(self):
        self.enunciados.append("Guardar la configuración hasta este momento.")
        self.ejercicio.copy_running_startup()

    def cambiar_prioridad_stp(self):
        prioridad_azar=randint(2, 12)
        nueva_prioridad=prioridad_azar * 4096
        plantilla="Cambiar la prioridad STP a {0}"
        self.enunciados.append(plantilla.format(nueva_prioridad))
        self.ejercicio.cambiar_prioridad_stp(nueva_prioridad)

    def generar_ejercicio(self, longitud):
        metodos=[
            self.poner_clave_admin,         self.poner_clave_telnet,
            self.configurar_ssh,            self.poner_hostname,
            self.poner_ip_azar,             self.poner_clave_consola_azar_con_login,
            #No tiene mucho sentido poner este
            #self.poner_clave_consola_azar_sin_login
            self.anadir_clave_mac_azar,     self.cambiar_timeout,
            self.mostrar_la_tabla_de_macs,  self.cambiar_prioridad_stp
        ]
        shuffle(metodos)
        for i in range(0, longitud):
            metodos[i]()
    
    def get_enunciado(self):
        enunciado="Configurar un switch Cisco mediante la línea de comandos cumpliendo los requisitos siguientes:\n\n"
        conpuntos=["* "+punto for punto in self.enunciados]
        return enunciado + "\n".join(conpuntos)

    def get_solucion(self):
        texto=self.get_enunciado()+"\n\n"
        texto+="La solución detallada sería esta::\n\n"
        con_prompt=["\t"+comando for comando in self.ejercicio.comandos_con_prompt]
        texto+="\n".join(con_prompt)

        texto+="\n\nLos comandos listos para copiar y pegar serían estos::\n\n"
        sin_prompt=["\t"+comando for comando in self.ejercicio.comandos_sin_prompt]
        texto+="\n".join(sin_prompt)
        return texto
        
    