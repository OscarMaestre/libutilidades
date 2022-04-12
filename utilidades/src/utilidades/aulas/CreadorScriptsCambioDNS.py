from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptCambioDNS(object):
    @staticmethod
    def crear(ruta_archivo_bat, ip, mascara,gateway, nombre_tarjeta_red):
        comando_dns_1="netsh interface ip set dns \"{3}\" static {4}" 
        comando_dns_2="netsh interface ip add dns \"{3}\" {5}" 
