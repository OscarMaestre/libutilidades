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
OTROS_PC=[100]
NOMBRES_OTROS_PC=["PROFESOR"]
NOMBRE_TARJETA_RED="Ethernet"

PLANTILLA_NOMBRE_AULA="AULAB{0}"
PLANTILLA_NOMBRE_PC="PC{0}"
PLANTILLA_NOMBRE_COMPLETO_ORDENADOR="{0}-{1}"

BITS_MASCARA=24

PLANTILLA_SCRIPT_IP="""
New-NetIPAddress –InterfaceAlias 'Ethernet' –IPv4Address '{0}' –PrefixLength {1} -DefaultGateway '{2}'
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
    ruta_script=get_ruta_script_pc(num_aula, num_pc, "02-Cambiar-IP.ps1")
    
    ip_final=PLANTILLA_IP.format(num_aula, num_pc)
    gw_final=GATEWAY.format(num_aula)
    texto_script=PLANTILLA_SCRIPT_IP.format(ip_final, BITS_MASCARA, gw_final)
    guardar_texto_en_archivo(ruta_script, texto_script)

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


if __name__=="__main__":
    crear_todo()