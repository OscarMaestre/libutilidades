class GestorMensajes(object):
    @staticmethod
    def get_cabecera(texto_cabecera):
        """Genera la cabecera de un archivo BAT"""
        PLANTILLA_CABECERA="""
@cls
@echo ************************************************************
@echo              {0}
@echo ************************************************************
        """
        texto=PLANTILLA_CABECERA.format(texto_cabecera)     
        return texto
    
    @staticmethod
    def get_mensaje(texto):
        PLANTILLA_MENSAJE="""
@echo.
@echo.
@echo {0}
@echo.
@echo.
    """
        texto=PLANTILLA_MENSAJE.format(texto)
        return texto

    @staticmethod
    def get_mensaje_con_pausa(texto):
        """Genera un mensaje que exigirá al usuario pulsar una tecla"""
        PLANTILLA="""
@echo.
{0}
@pause
"""
        mensaje_inicial=GestorMensajes.get_mensaje(texto)
        texto=PLANTILLA.format(mensaje_inicial)
        return texto