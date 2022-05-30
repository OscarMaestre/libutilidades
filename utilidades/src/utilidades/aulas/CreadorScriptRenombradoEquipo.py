from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptRenombradoEquipo(object):
    @staticmethod
    def crear(ruta_archivo_bat, nombre_equipo):
        
        PLANTILLA_CAMBIO_NOMBRE="NUEVO NOMBRE:{0}"
        texto_cabecera="Cambio del nombre del equipo"
        
        informe_comando_cambio_ip=PLANTILLA_CAMBIO_NOMBRE.format(nombre_equipo)
        
        texto_comando=GestorComandos.cambiar_nombre(nombre_equipo)
        
        texto_mensaje_espera="Comprueba si ha habido algún error conocido. Si no es así, pulsa una tecla para acabar Y REINICIA EL EQUIPO PARA QUE EL CAMBIO TENGA EFECTO"

        CreadorScriptsBat.crear(ruta_archivo_bat, texto_cabecera, informe_comando_cambio_ip, texto_comando, texto_mensaje_espera)
        