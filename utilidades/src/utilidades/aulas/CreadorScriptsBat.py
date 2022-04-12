from os import stat
from utilidades.aulas.GestorMensajes import GestorMensajes

class CreadorScriptsBat(object):
    @staticmethod
    def crear(ruta_archivo, cabecera, informe, comando, texto_cierre) -> None:
        PLANTILLA_BAT="""
        {0}

        {1}

        {2}

        {3}
        """
        texto_cabecera=GestorMensajes.get_cabecera(cabecera)
        texto_informe=GestorMensajes.get_mensaje_con_pausa(informe)
        texto_cierre=GestorMensajes.get_mensaje_con_pausa(texto_cierre)

        archivo_bat=PLANTILLA_BAT.format(
            texto_cabecera, texto_informe, comando, texto_cierre
        )
        with open(ruta_archivo, "w") as fich:
            fich.write(archivo_bat)