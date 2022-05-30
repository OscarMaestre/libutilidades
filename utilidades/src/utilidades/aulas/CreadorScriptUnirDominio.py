from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptUnirDominio(object):
    @staticmethod
    def crear(ruta_archivo_bat):
        
        
        texto_cabecera="Uniendo al dominio ciclos.local"
        
        informe_union_dominio="Se va a unir este equipo al dominio."
        
        texto_comando=GestorComandos.unir_a_dominio()
        
        texto_mensaje_espera="Comprueba si ha habido algún error conocido. Si no es así, pulsa una tecla para acabar."

        CreadorScriptsBat.crear(ruta_archivo_bat, texto_cabecera, informe_union_dominio, texto_comando, texto_mensaje_espera)
        
        
