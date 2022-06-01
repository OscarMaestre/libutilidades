from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptPermisos(object):
    @staticmethod
    def crear(ruta_archivo_bat, usuario):
        
        
        texto_cabecera="ASIGNADOR DE PERMISOS EN DISCO"
        
        informe_union_dominio="Se va a asignar un disco al usuario {0}.".format(usuario)
        
        texto_comando=GestorComandos.dar_propiedad_disco_a_alumno(usuario)
        
        texto_mensaje_espera="Comprueba si ha habido algún error conocido. Si no es así, puedes terminar la ejecución"

        CreadorScriptsBat.crear(ruta_archivo_bat, texto_cabecera, informe_union_dominio, texto_comando, texto_mensaje_espera)
        
        
