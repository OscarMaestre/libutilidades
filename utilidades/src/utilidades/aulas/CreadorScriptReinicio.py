from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptReinicio(object):
    @staticmethod
    def crear(ruta_archivo_bat):
        
        
        texto_cabecera="Reiniciando..."
        
        informe_union_dominio="En este punto ES IMPRESCINDIBLE REINICIAR EL EQUIPO"
        
        texto_comando=GestorComandos.reiniciar_equipo()
        
        texto_mensaje_espera="Comprueba si ha habido algún error conocido. Si no es así, puedes terminar la ejecución y esperar (se tardan 30-45 segundos)"

        CreadorScriptsBat.crear(ruta_archivo_bat, texto_cabecera, informe_union_dominio, texto_comando, texto_mensaje_espera)
        
        
