from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptCambioIP(object):
    @staticmethod
    def crear(ruta_archivo_bat, ip, mascara,gateway, nombre_tarjeta_red):
        
        PLANTILLA_DATOS_IP="NUEVOS DATOS IP Tarjeta:'{3}', IP:{0} / {1}, Puerta enlace:{2}"
        texto_cabecera="Cambio de la direccion IP"
        
        informe_comando_cambio_ip=PLANTILLA_DATOS_IP.format(ip, mascara, gateway, nombre_tarjeta_red)
        
        texto_comando=GestorComandos.set_ip(ip, mascara, gateway, nombre_tarjeta_red)
        
        texto_mensaje_espera="Comprueba si ha habido algún error conocido. Si no es así, pulsa una tecla para acabar."

        CreadorScriptsBat.crear(ruta_archivo_bat, texto_cabecera, informe_comando_cambio_ip, texto_comando, texto_mensaje_espera)
        