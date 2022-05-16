from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptCambioDNS(object):
    @staticmethod
    def crear(ruta_archivo_bat,nombre_tarjeta_red, dns1, dns2):
        
        PLANTILLA_DATOS_DNS="NUEVOS DATOS DNS Tarjeta:'{2}',DNS 1: {0}, DNS 2: {1}"
        texto_cabecera="Cambio de los DNS"
        
        informe_cambio_dns=PLANTILLA_DATOS_DNS.format(dns1, dns2, nombre_tarjeta_red)
        
        texto_comando=GestorComandos.cambiar_dns(dns1, dns2, nombre_tarjeta_red)
        
        texto_mensaje_espera="Comprueba si ha habido algún error conocido. Si no es así, pulsa una tecla para acabar."

        CreadorScriptsBat.crear(ruta_archivo_bat, texto_cabecera, informe_cambio_dns, texto_comando, texto_mensaje_espera)
        
        


