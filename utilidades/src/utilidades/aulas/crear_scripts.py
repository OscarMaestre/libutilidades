from os import mkdir
from os.path import join
# Cosas que hacer al hacer la imagen
# Tener a mano el usuario administrador y la clave
# Habilitar la ejecución de scripts ejecutando esto como administrador
#               
#                   Set-ExecutionPolicy Unrestricted -Scope LocalMachine -Force

MIN_AULA=8
MAX_AULA=15

MIN_PC=1
MAX_PC=20

#Si hay otros ordenadores con otras IP poner aquí su último byte y su nombre
#Por ejemplo, el PC con la IP xxx.xxx.xxx.100 suele ser el "PC-PROFESOR"
OTROS_PC=[100, 101]
NOMBRES_OTROS_PC=["PROFESOR", "BORRAR"]


#Pon aquí el nombre que tenga la tarjeta de red en Windows
NOMBRE_TARJETA_RED="Ethernet"

# Plantillas para los nombres de los equipos. 
# En principio los equipos se llaman algo como AULAB09-PC04
# Todo tiene dos digitos y si no los hay se rellena con 0, ejemplo PC04 o PC17
PLANTILLA_NOMBRE_AULA="AULAB{0}"
PLANTILLA_NOMBRE_PC="PC{0}"
PLANTILLA_NOMBRE_COMPLETO_ORDENADOR="{0}-{1}"

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


PLANTILLA_SCRIPT_CAMBIAR_CLAVE_USUARIO="""
@echo off
@echo.
@echo.
@echo.
@echo Se va a proceder a cambiar la clave del usuario {0} y se le va a poner la clave {1}
@pause
net user {0} {1}
@echo.
@echo.
@echo.
@echo Comprueba si hay algún error y pulsa una tecla
@echo.
@echo.
@echo.
@pause
"""

PLANTILLA_COMANDO_RENOMBRAR_EQUIPO="""
@echo *******************************************************************
@echo                      Renombrado del equipo
@echo *******************************************************************

@echo.
@echo.
@echo.
@echo Se va cambiar el nombre de este ordenador y despues vamos a reiniciar el equipo (es obligatorio)
@echo.
@echo El nuevo nombre que se va a poner es {0}
@echo.
@pause

WMIC ComputerSystem where Name="%COMPUTERNAME%" call Rename Name="{0}"
@echo.
@echo.
@echo.
@echo SI HAY ERRORES PULSA AHORA MISMO CTRL+C.
@echo SI NO HAY ERRORES PULSA UNA TECLA Y REINICIAREMOS EL EQUIPO
@pause
shutdown /r
"""
PLANTILLA_UNIR_DOMINIO  ="""
@echo ******************************************************************
@echo *                Union al dominio                                *
@echo ******************************************************************
@echo.
@echo.
@echo.
@echo Se va a proceder a unir este equipo al dominio del Pabellon B.
@echo Por favor repasa los datos siguientes antes de ejecutar esto
@echo Se va a ejecutar esto
@echo netdom.exe join %computername% /domain:{0} /UserD:{1}\{2} /PasswordD:{3} /reboot
@echo.
@echo.
@pause
netdom.exe join %computername% /domain:{0} /UserD:{1}\{2} /PasswordD:{3} /reboot
@echo.
@echo.
@echo.
@pause
"""



def get_numero_con_ceros(numero):
    cadena=str(numero)
    cadena_con_ceros=cadena.zfill(2)
    return cadena_con_ceros

def get_otros_nombres_equipo(num_pc):
    for pos, valor in enumerate(OTROS_PC):
        if valor==num_pc:
            return NOMBRES_OTROS_PC[pos]
    return "DESCONOCIDO"

def get_nombre_aula(num_aula):
    return PLANTILLA_NOMBRE_AULA.format(get_numero_con_ceros(num_aula))

def get_nombre_pc(num_pc):
    return PLANTILLA_NOMBRE_PC.format(get_numero_con_ceros(num_pc))

def get_nombre_completo_pc(num_aula, num_pc):
    #print(num_pc)
    if num_pc>MAX_PC:
        num_pc=get_otros_nombres_equipo(num_pc)
    nombre_aula=get_nombre_aula(num_aula)
    nombre_pc=get_nombre_pc(num_pc)

    texto=PLANTILLA_NOMBRE_COMPLETO_ORDENADOR.format(nombre_aula, nombre_pc)
    return texto

def crear_directorio_si_no_existe(ruta):
    try:
        mkdir(ruta)
    except FileExistsError:
        pass

def get_ruta_directorio_equipo(num_aula, num_pc):
    nombre_aula=get_nombre_aula(num_aula)
    nombre_pc=get_nombre_pc(num_pc)
    ruta=join(nombre_aula, nombre_pc)
    return ruta

def crear_directorio_equipo(num_aula, num_pc):
    nombre_dir=get_ruta_directorio_equipo(num_aula, num_pc)
    crear_directorio_si_no_existe(nombre_dir)

def guardar_texto_en_archivo(ruta, texto):
    with open(ruta, "w") as fich:
        fich.write(texto)


def get_ruta_script_pc(num_aula, num_pc, nombre_fichero):
    directorio_base=get_ruta_directorio_equipo(num_aula, num_pc)
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
    ruta_script=get_ruta_script_pc(num_aula, num_pc, "02-Cambiar-IP.bat")
    
    ip_final=PLANTILLA_IP.format(num_aula, num_pc)
    gw_final=GATEWAY.format(num_aula)
    texto_script=PLANTILLA_SCRIPT_IP.format(ip_final, MASCARA, gw_final, NOMBRE_TARJETA_RED, IP_DNS_1, IP_DNS_2)
    guardar_texto_en_archivo(ruta_script, texto_script)

def crear_script_cambio_clave(num_aula, num_pc, usuario, clave):
    comando_cambio_clave=PLANTILLA_SCRIPT_CAMBIAR_CLAVE_USUARIO.format(usuario, clave)
    nombre_script_cambio_clave="03-Cambiar-clave-profesor-a-Inf-678.bat"
    ruta_script=get_ruta_script_pc(num_aula, num_pc, nombre_script_cambio_clave)
    guardar_texto_en_archivo(ruta_script, comando_cambio_clave)

def crear_script_renombrado_equipo(num_aula, num_pc):
    nombre_equipo=get_nombre_completo_pc(num_aula, num_pc)
    comando=PLANTILLA_COMANDO_RENOMBRAR_EQUIPO.format(nombre_equipo)
    nombre_script_renombrado="04-Renombrar el equipo.bat"
    ruta_script=get_ruta_script_pc(num_aula, num_pc, nombre_script_renombrado)
    guardar_texto_en_archivo(ruta_script, comando)

def crear_script_union_dominio(num_aula, num_pc, nombre_dominio, admin_dominio, clave_admin_dominio):
    nombre_script_cambio_clave="05-Unir al dominio.bat"
    ruta_script=get_ruta_script_pc(num_aula, num_pc, nombre_script_cambio_clave)
    comando_unir_dominio=PLANTILLA_UNIR_DOMINIO.format(nombre_dominio, nombre_dominio, admin_dominio, clave_admin_dominio)
    guardar_texto_en_archivo(ruta_script, comando_unir_dominio)


def crear_todo():
    numeros_aula=range(MIN_AULA, MAX_AULA+1)
    num_ordenador=range(MIN_PC, MAX_PC+1)
    posibles_ordenadores=list(num_ordenador)+OTROS_PC

    #Para cada aula
    for aula_sin_ceros in numeros_aula:
        aula_con_ceros=get_numero_con_ceros(aula_sin_ceros)
        directorio_aula=get_nombre_aula(aula_sin_ceros)
        crear_directorio_si_no_existe(directorio_aula)
        #Para cada ordenador de esa aula
        for num_pc in posibles_ordenadores:
            nombre=get_nombre_completo_pc(aula_sin_ceros, num_pc)
            print(nombre)
            crear_directorio_equipo(aula_con_ceros, num_pc)
            
            crear_script_habilitacion(aula_sin_ceros, num_pc)
            crear_script_cambio_ip(aula_sin_ceros, num_pc)
            crear_script_cambio_clave(aula_sin_ceros, num_pc, NOMBRE_USUARIO_PROFESOR, CLAVE_USUARIO_LOCAL_PROFESOR)
            crear_script_renombrado_equipo(aula_sin_ceros, num_pc)
            crear_script_union_dominio(aula_sin_ceros, num_pc, "ciclos.local", "admin", "19+Ipf-20")


if __name__=="__main__":
    crear_todo()