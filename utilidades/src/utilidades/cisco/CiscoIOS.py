from random import choice
class CiscoIOS(object):
    #Estado del switch o router
    MODO_USUARIO=1
    MODO_ADMIN  = MODO_USUARIO + 1
    MODO_CONFIG = MODO_ADMIN   + 1
    MODO_4       =MODO_CONFIG  + 1
    
    def __init__(self, estado_inicial=MODO_USUARIO, nombre_inicial="Switch1") -> None:
        self.comandos_con_prompt=[]
        self.comandos_sin_prompt=[]
        self.modo=estado_inicial
        self.nombre=nombre_inicial
        self.texto_modo=""
    
    def get_modo(self):
        return self.modo

    def anadir_comando(self, comando):
        # print("Modo actual:"+str(self.modo))
        # print("Apilando comando:"+comando)
        if self.modo==CiscoIOS.MODO_USUARIO:
            self.comandos_con_prompt.append( "{0}>{1}".format(self.nombre, comando ) )
        if self.modo==CiscoIOS.MODO_ADMIN:
            self.comandos_con_prompt.append( "{0}#{1}".format(self.nombre, comando ) )
        if self.modo>CiscoIOS.MODO_ADMIN:
            self.comandos_con_prompt.append( "{0}({2})#{1}".format(self.nombre, comando, self.texto_modo ) )
        self.comandos_sin_prompt.append( "{0}".format( comando ) )

    def enable(self):
        self.anadir_comando("enable")
        self.activar_modo_admin()

    def configure_terminal(self):
        self.anadir_comando("configure terminal")
        self.activar_modo_config()

    def exit(self):
        self.anadir_comando("exit")
        
    
    def activar_modo_config(self):
        self.texto_modo="config"
        self.modo=CiscoIOS.MODO_CONFIG
    
    def activar_modo_admin(self):
        self.texto_modo=""
        self.modo=CiscoIOS.MODO_ADMIN
    
    def activar_modo_usuario(self):
        self.texto_modo=""
        self.modo=CiscoIOS.MODO_USUARIO

    def ir_a_modo_usuario(self):
        if self.modo==CiscoIOS.MODO_ADMIN:
            self.exit()
            self.activar_modo_usuario()
        if self.modo==CiscoIOS.MODO_USUARIO:
            return 
        if self.modo==CiscoIOS.MODO_CONFIG:
            self.exit()
            self.activar_modo_admin()
            self.exit()
            self.activar_modo_usuario()

        if self.MODO_4==CiscoIOS.MODO_4:
            self.exit()
            self.activar_modo_config()
            self.exit()
            self.activar_modo_admin()
            self.exit()
            self.activar_modo_usuario()

    def ir_a_modo_admin(self):
        if self.modo==CiscoIOS.MODO_ADMIN:
            return
        if self.modo==CiscoIOS.MODO_USUARIO:
            self.enable()
        if self.modo==CiscoIOS.MODO_CONFIG:
            self.exit()
            self.activar_modo_admin()
        if self.modo==CiscoIOS.MODO_4:
            self.exit()
            self.activar_modo_config()
            self.exit()
            self.activar_modo_admin()
            

    def ir_a_modo_config(self):
        
        if self.modo==CiscoIOS.MODO_CONFIG:
            return 
        if self.modo==CiscoIOS.MODO_ADMIN:
            self.configure_terminal()
        if self.modo==CiscoIOS.MODO_USUARIO:
            self.enable()
            self.configure_terminal()
        if self.modo==CiscoIOS.MODO_4:
            self.exit()
        self.activar_modo_config()

    def ir_a_modo_4(self, comando, texto):
        #print("Yendo a modo 4 desde modo:"+str(self.modo))
        if self.modo==CiscoIOS.MODO_CONFIG:
            pass
        if self.modo==CiscoIOS.MODO_ADMIN:
            self.configure_terminal()
        if self.modo==CiscoIOS.MODO_USUARIO:
            self.enable()
            self.configure_terminal()
        if self.modo==CiscoIOS.MODO_4:
            pass
        
        
        self.anadir_comando(comando)
        self.texto_modo=texto
        self.modo=CiscoIOS.MODO_4

    def copy_running_startup(self):
        self.ir_a_modo_admin()
        self.anadir_comando("copy running-config startup-config")

    def hostname(self, nuevo_nombre):
        
        self.ir_a_modo_config()
        #print("Nuevo modo:"+str(self.modo))
        self.anadir_comando("hostname " + nuevo_nombre)
        self.nombre=nuevo_nombre
        
    def get_comandos_con_prompt(self):
        return "\n".join(self.comandos_con_prompt)


    def cambiar_prioridad_stp(self, prioridad):
        self.ir_a_modo_config()
        plantilla="spanning tree vlan 1 priority {0}"
        self.anadir_comando(plantilla.format(str(prioridad)))

    def get_comandos_sin_prompt(self):
        return "\n".join(self.comandos_sin_prompt)

    def poner_clave_consola_sin_login(self, clave):
        self.ir_a_modo_4("line console 0", "config-line")
        self.anadir_comando("password " + clave)
    
    def login(self):
        self.anadir_comando("login")

    def poner_clave_consola_con_login(self, clave):
        self.ir_a_modo_config()
        self.ir_a_modo_4("line console 0", "config-line")
        self.anadir_comando("password " + clave)
        self.login()

    def poner_clave_admin(self, clave):
        self.ir_a_modo_config()
        self.anadir_comando("enable secret "+clave)

    def poner_clave_telnet(self, clave):
        self.ir_a_modo_config()
        self.ir_a_modo_4("line vty 0 15", "config-line")
        self.anadir_comando("password "+clave)
        self.login()


    def poner_ip_gestion(self, ip, mascara):
        self.ir_a_modo_4("interface vlan 1", "config-if")
        
        self.anadir_comando("ip address "+ ip + " " + mascara)
        self.anadir_comando("no shutdown")

    def generar_claves_publicas(self, dominio, longitud_clave):
        self.ir_a_modo_config()
        self.anadir_comando("ip domain-name "+dominio)
        self.anadir_comando("crypto key generate rsa general-keys modulus "+str(longitud_clave))

    def configurar_usuario_ssh(self, usuario, clave):
        self.ir_a_modo_config()
        self.anadir_comando(
            "username {0} secret {1}".format(usuario, clave)
        )
        self.ir_a_modo_4("line vty 0 15", "config-line")
        self.anadir_comando("login local")
        self.anadir_comando("transport input ssh")

    def cambiar_timeout_arp(self, segundos):
        self.ir_a_modo_4("interface vlan 1", "config-if")
        self.anadir_comando("arp timeout "+str(segundos))
        self.anadir_comando("no shutdown")

    def anadir_mac_puerto(self, mac, num_puerto):
        self.ir_a_modo_config()
        comando="mac address-table static {0} vlan 1 interface fastEthernet 0/{1}"
        self.anadir_comando( comando.format(mac, str(num_puerto)) )

    def ver_tabla_macs(self):
        self.ir_a_modo_admin()
        self.anadir_comando("show mac-address-table")
    
    def get_cifras_hexadecimales(self, longitud):
        cifras="0123456789abcdef"
        bloque=""
        for i in range(0, longitud):
            bloque=bloque+choice(cifras)
        return bloque


    def generar_mac_azar(self):
        bloque0="00aa"
        bloque1=self.get_cifras_hexadecimales(4)
        bloque2=self.get_cifras_hexadecimales(4)
        return ".".join([bloque0, bloque1, bloque2])

    def poner_dominio_vtp(self, nombre_dominio):
        self.ir_a_modo_config()
        self.anadir_comando("vtp domain "+ nombre_dominio)

    def poner_clave_vtp(self, clave):
        self.ir_a_modo_config()
        self.anadir_comando("vtp password "+ clave)

    def vtp_server(self):
        self.ir_a_modo_config()
        self.anadir_comando("vtp mode server")
    
    def vtp_client(self):
        self.ir_a_modo_config()
        self.anadir_comando("vtp mode client")

    def vtp_transparent(self):
        self.ir_a_modo_config()
        self.anadir_comando("vtp mode transparent")
    
    def poner_vtp_modo_servidor(self, dominio, clave):
        self.poner_dominio_vtp(dominio)
        self.poner_clave_vtp(clave)
        self.vtp_server()

    def poner_vtp_modo_cliente(self, dominio, clave):
        self.poner_dominio_vtp(dominio)
        self.poner_clave_vtp(clave)
        self.vtp_client()
    
    def crear_vlan(self, numero, nombre):
        self.ir_a_modo_4("vlan "+str(numero), "config-vlan")
        self.anadir_comando("name "+nombre)
        

    def poner_interfaz_acceso(self, num_interfaz, id_vlan):
        interfaz="interface FastEthernet 0/"+str(num_interfaz)
        self.ir_a_modo_4(interfaz, "config-if")
        self.anadir_comando("switchport mode access")
        self.anadir_comando("switchport access vlan "+str(id_vlan))
        self.ir_a_modo_config()

    def poner_interfaz_troncal(self, num_interfaz, id_vlan):
        interfaz="interface FastEthernet 0/"+str(num_interfaz)
        self.ir_a_modo_4(interfaz, "config-if")
        self.anadir_comando("switchport mode trunk")
        self.anadir_comando("switchport trunk allowed vlan "+str(id_vlan))
        self.ir_a_modo_config()

    def poner_interfaz_troncal_lista(self, num_interfaz, lista_vlans):
        cadena_vlans=",".join(lista_vlans)
        interfaz="interface FastEthernet 0/"+str(num_interfaz)
        self.ir_a_modo_4(interfaz, "config-if")
        self.anadir_comando("switchport mode trunk")
        self.anadir_comando("switchport trunk allowed vlan "+cadena_vlans)

    def mostrar_vlans(self):
        self.ir_a_modo_config()
        self.anadir_comando("show vlan")
        
        