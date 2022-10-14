from os import stat
from utilidades.aulas.GestorMensajes import GestorMensajes

class CreadorScriptsBat(object):
    @staticmethod
    def crear(ruta_archivo, cabecera, informe, comando, texto_cierre) -> None:
        PLANTILLA_BAT="""
        {0}

        {1}

        {2}

        {3}
        """
        texto_cabecera=GestorMensajes.get_cabecera(cabecera)
        texto_informe=GestorMensajes.get_mensaje_con_pausa(informe)
        texto_cierre=GestorMensajes.get_mensaje_con_pausa(texto_cierre)

        archivo_bat=PLANTILLA_BAT.format(
            texto_cabecera, texto_informe, comando, texto_cierre
        )
        with open(ruta_archivo, "w") as fich:
            fich.write(archivo_bat)


class ArchivoBAT(object):
    def __init__(self) -> None:
        self.lineas=[]

    def echo_off(self):
        self.lineas.append("@echo off")
    
    def anadir_linea_en_blanco(self):
        self.lineas.append("echo.")
    
    def pause(self):
        self.lineas.append("@pause")

    def get_texto(self):
        texto="\n".join(self.lineas)
        return texto
    
    def anadir_echo(self, texto):
        self.lineas.append("@echo "+texto)

    def anadir_cabecera(self, linea):
        ANCHO_LINEA=60
        asteriscos="*"*ANCHO_LINEA
        linea_asteriscos_en_blanco="*"+" "*ANCHO_LINEA-2 + "*"
        self.anadir_echo(asteriscos)
        self.anadir_echo(linea_asteriscos_en_blanco)
        self.anadir_echo(linea_asteriscos_en_blanco)
        linea_centrada="*"++linea.center(ANCHO_LINEA-2)+"*"
        self.anadir_echo(linea_centrada)
        self.anadir_echo(linea_asteriscos_en_blanco)
        self.anadir_echo(linea_asteriscos_en_blanco)
        self.anadir_echo(asteriscos)

    def set_ip(self, ip, mascara, gateway, nombre_tarjeta="Ethernet"):
        PLANTILLA="netsh interface ip set address name= \"{3}\" static {0} {1} {2}"
        texto=PLANTILLA.format(ip, mascara, gateway, nombre_tarjeta)
        self.lineas.append(texto)

    def cambiar_dns(self, dns1, dns2, nombre_tarjeta="Ethernet"):
        PLANTILLA_DNS="""
{0}
{1}
"""
        comando_dns_1="netsh interface ip set dns \"{0}\" static {1}" 
        comando_dns_2="netsh interface ip add dns \"{0}\" {1}"
        comando1=comando_dns_1.format(nombre_tarjeta, dns1)
        comando2=comando_dns_2.format(nombre_tarjeta, dns2)
        texto=PLANTILLA_DNS.format(comando1, comando2)
        self.lineas.append(texto)