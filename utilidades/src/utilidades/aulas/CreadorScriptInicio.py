from utilidades.aulas.GestorComandos import GestorComandos
from utilidades.aulas.CreadorScriptsBat import CreadorScriptsBat

class CreadorScriptInicio(object):
    @staticmethod
    def crear(ruta_archivo_bat):

        texto_archivo="""


@echo.
@cls
@echo *********************************************************
@echo *                                                       *
@echo *                                                       *
@echo *           CONFIGURACION INICIAL DEL EQUIPO            *
@echo *                                                       *
@echo *                                                       *
@echo *                                                       *
@echo *                                                       *
@echo *********************************************************
@echo.
@echo.
@echo.
@echo Este script no hace nada en particular, solo es para 
@echo recordarte lo siguiente:
@echo     * Los script deben ejecutarse por orden.
@echo     * Debes ejecutarlos COMO ADMINISTRADOR (recuerda que
@echo         si quieres puedes usar el boton derecho encima
@echo         del script y elegir -Ejecutar como administrador-)
@echo     * El cambio de direccion IP puede fallar. Parece que
@echo         en general Windows asume que las tarjetas de red
@echo         se llaman -Ethernet- pero no siempre ocurre. Si
@echo         el cambio de IP falla, hay que hacerlo a mano.
@echo     * El cambio de permisos de discos tambien hay que 
@echo         hacerlo a mano.
@echo.
@echo.
@pause        
"""

        with open(ruta_archivo_bat, "w") as fich:
            fich.write(texto_archivo)
        