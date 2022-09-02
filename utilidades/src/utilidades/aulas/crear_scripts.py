from os import makedirs, mkdir
from os.path import join
from tkinter import dnd

from utilidades.aulas.GestorNombres import GestorNombres

from utilidades.aulas.CreadorScriptCambioIP import CreadorScriptCambioIP

from utilidades.aulas.CreadorScriptsCambioDNS import CreadorScriptCambioDNS

from utilidades.aulas.CreadorScriptCambioClave import CreadorScriptCambioClave

from utilidades.aulas.CreadorScriptUnirDominio import CreadorScriptUnirDominio

from utilidades.aulas.CreadorScriptRenombradoEquipo import CreadorScriptRenombradoEquipo

from utilidades.aulas.CreadorScriptPermisos import CreadorScriptPermisos

from utilidades.aulas.CreadorScriptReinicio import CreadorScriptReinicio

# Cosas que hacer al hacer la imagen
# Tener a mano el usuario administrador y la clave
# Habilitar la ejecución de scripts ejecutando esto como administrador
#               
#                   Set-ExecutionPolicy Unrestricted -Scope LocalMachine -Force

MIN_AULA=8
MAX_AULA=15

MIN_PC=1
MAX_PC=32



#Pon aquí el nombre que tenga la tarjeta de red en Windows
NOMBRE_TARJETA_RED="Ethernet"


#Los bits de mascara se usan en Powershell
BITS_MASCARA=24
#La mascara en decimal se usa en MS-DOS
MASCARA="255.255.255.0"
NOMBRE_TARJETA_RED="Ethernet"

IP_DNS_1="10.1.0.1"
IP_DNS_2="8.8.8.8"

NOMBRE_USUARIO_PROFESOR="profesor"
CLAVE_USUARIO_LOCAL_PROFESOR="inf-678"

#Esto se podrá usar más adelante, cuando declaren obsoleto el netsh
POWER_SHELL_PLANTILLA_SCRIPT_IP="""
New-NetIPAddress –InterfaceAlias 'Ethernet' –IPAddress '{0}' –PrefixLength {1} -DefaultGateway '{2}'
read-host "Pulsa una tecla"
"""

PLANTILLA_SCRIPT_IP="""
netsh interface ip set address name= \"{3}\" static {0} {1} {2}
@echo Comprueba si hay algún error y pulsa una tecla 
@pause
@echo.
@echo.
@echo.
@echo Ahora vamos a poner los DNS (Si devuelve un mensaje como parametro incorrecto puedes ignorarlo)
netsh interface ip set dns "{3}\" static {4} 
netsh interface ip add dns \"{3}\" {5} 
@echo.
@echo.
@echo.
@echo.
@echo Comprueba si hay algún error y luego pulsa una tecla. Si hay un error puedes pulsar Ctrl+C para no seguir
@echo.
@echo.
@pause
@cls
@echo Ahora vamos a ejecutar IPCONFIG para ver si la configuración está bien
@pause
@cls
@ipconfig
@pause
@cls
@echo Vamos a ejecutar algún ping para ver si la red funciona.
@pause
@set ip={2}
@echo Ejecutando ping...
@echo.
@echo.
@echo.
ping -n 1 %ip% | find "TTL"
@pause
@if not errorlevel 1 set error="Parece que ping ha funcionado y todo ha ido bien"
@if errorlevel 1 set error="Parece que ping ha fallado, comprueba si la IP estaba bien, si el cable del PC está puesto y si el switch está encendido"
@cls
@echo.
@echo *****************************************************
@echo %error%
@echo *****************************************************
@echo.

@echo.
@echo Pulsa una tecla para finalizar la ejecución
@echo.
@echo.
@pause
"""






def get_numero_con_ceros(numero):
    cadena=str(numero)
    cadena_con_ceros=cadena.zfill(2)
    return cadena_con_ceros




def crear_directorio_si_no_existe(ruta):
    try:
        makedirs(ruta)
    except FileExistsError:
        pass

def crear_directorio_equipo(nombre_aula, nombre_pc):
    nombre_dir=join(nombre_aula, nombre_pc)
    print(nombre_dir)
    crear_directorio_si_no_existe(nombre_dir)

def guardar_texto_en_archivo(ruta, texto):
    with open(ruta, "w") as fich:
        fich.write(texto)


def get_ruta_script_pc(num_aula, num_pc, nombre_fichero):
    gestor_nombres=GestorNombres(num_aula, num_pc)
    nombre_aula=gestor_nombres.get_nombre_aula()
    nombre_pc=gestor_nombres.get_nombre_pc()
    directorio_base=join(nombre_aula, nombre_pc)
    ruta_completa=join(directorio_base, nombre_fichero)
    return ruta_completa

def crear_script_habilitacion(num_aula, num_pc):
    ruta=get_ruta_script_pc(num_aula, num_pc, "01-Habilitar-Powershell.ps1")
    texto="Set-ExecutionPolicy Unrestricted -Scope LocalMachine -Force"
    guardar_texto_en_archivo(ruta, texto)

def crear_script_cambio_ip(num_aula, num_pc):
    PLANTILLA_IP="10.{0}.0.{1}"
    GATEWAY="10.{0}.0.254"
    DNS=["10.1.0.1", "8.8.4.4"]

    ip=PLANTILLA_IP.format(num_aula, num_pc)
    mascara="255.255.0.0"
    gateway=GATEWAY.format(num_aula)

    ruta_script=get_ruta_script_pc(num_aula, num_pc, "02-Cambiar-IP.bat")
    CreadorScriptCambioIP.crear(ruta_script, ip, mascara, gateway, NOMBRE_TARJETA_RED)
    #guardar_texto_en_archivo(ruta_script, texto_script)

def crear_script_cambio_dns(num_aula, num_pc):
    DNS=["10.1.0.1", "8.8.4.4"]
    ruta_script=get_ruta_script_pc(num_aula, num_pc, "03-Cambiar-DNS.bat")
    CreadorScriptCambioDNS.crear(ruta_script, NOMBRE_TARJETA_RED, DNS[0], DNS[1] )
    
def crear_script_cambio_clave(num_aula, num_pc, usuario, clave):
    nombre_script_cambio_clave="04-Cambiar-clave-profesor-a-{0}.bat".format(clave)
    ruta_script=get_ruta_script_pc(num_aula, num_pc, nombre_script_cambio_clave)
    CreadorScriptCambioClave.crear(ruta_script, usuario, clave)

def crear_script_renombrado_equipo(num_aula, num_pc):
    gestor_nombres=GestorNombres(num_aula, num_pc)
    ruta_script=get_ruta_script_pc(num_aula, num_pc, "05-Renombrar-equipo.bat")
    CreadorScriptRenombradoEquipo.crear(ruta_script, gestor_nombres.get_nombre_completo_pc())
    return
    #guardar_texto_en_archivo(ruta_script, comando)

def crear_script_union_dominio(num_aula, num_pc):
    nombre_script_cambio_clave="07-Unir-a-dominio.bat"
    ruta_script=get_ruta_script_pc(num_aula, num_pc, nombre_script_cambio_clave)
    CreadorScriptUnirDominio.crear(ruta_script)

def crear_script_disco_manana(num_aula, num_pc):
    gestor_nombres=GestorNombres(num_aula, num_pc)
    ruta_script=get_ruta_script_pc(num_aula, num_pc, "09-Disco-del-usuario-manana.bat")
    CreadorScriptPermisos.crear(ruta_script, gestor_nombres.get_nombre_completo_pc(), gestor_nombres.get_nombre_alumno("M"))

def crear_script_reinicio(num_aula, num_pc, nombre_bat):
    gestor_nombres=GestorNombres(num_aula, num_pc)
    ruta_script=get_ruta_script_pc(num_aula, num_pc, nombre_bat)
    CreadorScriptReinicio.crear(ruta_script)


def crear_script_disco_tarde(num_aula, num_pc):
    gestor_nombres=GestorNombres(num_aula, num_pc)
    ruta_script=get_ruta_script_pc(num_aula, num_pc, "10-Disco-del-usuario-tarde.bat")
    CreadorScriptPermisos.crear(ruta_script, gestor_nombres.get_nombre_completo_pc(), gestor_nombres.get_nombre_alumno("T"))


def crear_todo():
    numeros_aula=range(MIN_AULA, MAX_AULA+1)
    num_ordenador=range(MIN_PC, MAX_PC+1)
    posibles_ordenadores=list(num_ordenador)+[100]
    #Para cada aula
    for aula_sin_ceros in numeros_aula:
        #Para cada ordenador de esa aula
        for num_pc in posibles_ordenadores:
            gestor_nombres=GestorNombres(aula_sin_ceros, num_pc)
            crear_directorio_equipo(gestor_nombres.get_nombre_aula(), gestor_nombres.get_nombre_pc())
            crear_script_cambio_ip(aula_sin_ceros, num_pc)
            crear_script_cambio_dns(aula_sin_ceros, num_pc)
            crear_script_renombrado_equipo(aula_sin_ceros, num_pc)
            crear_script_reinicio(aula_sin_ceros, num_pc, "06-Reiniciar.bat")
            crear_script_cambio_clave(aula_sin_ceros, num_pc, NOMBRE_USUARIO_PROFESOR, CLAVE_USUARIO_LOCAL_PROFESOR)
            crear_script_union_dominio(aula_sin_ceros, num_pc)
            crear_script_reinicio(aula_sin_ceros, num_pc, "08-Reiniciar.bat")
            #crear_script_disco_manana(aula_sin_ceros, num_pc)
            #crear_script_disco_tarde(aula_sin_ceros, num_pc)


if __name__=="__main__":
    crear_todo()