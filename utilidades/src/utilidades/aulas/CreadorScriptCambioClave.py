from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptCambioClave(object):
    @staticmethod
    def crear(ruta_archivo_bat,usuario, nueva_clave):
        

        texto_cabecera="Cambio de clave para el usuario "+usuario

        PLANTILLA_INFORME="Se va a cambiar la clave al usuario {0} y ahora tendrá la clave {1}"
        informe_cambio_dns=PLANTILLA_INFORME.format(usuario, nueva_clave)
        texto_comando=GestorComandos.cambiar_clave(usuario, nueva_clave)

        texto_mensaje_espera="Comprueba si ha habido algún error conocido. Si no es así, pulsa una tecla para acabar."

        CreadorScriptsBat.crear(ruta_archivo_bat, texto_cabecera, informe_cambio_dns, texto_comando, texto_mensaje_espera)
        
        
