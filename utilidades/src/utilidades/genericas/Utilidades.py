from random import randint
import telegram_send

class Utilidades(object):
    @staticmethod
    def enviar_mensaje_por_telegram(mensaje):
        """
        
        Envía un mensaje a través del BotAvisador
        
        Argumentos:
        
            mensaje -- Mensaje  a enviar
        """
        telegram_send.send(messages=[mensaje])

    @staticmethod
    def elegir_elemento_al_azar(lista):
        """
        
        Devuelve un elemento al azar de una lista
        
        Argumentos:
        
            lista -- Lista con elementos

        Devuelve

            Un elemento cualquiera de la lista o error si la lista está vacía

        """

        if len(lista)==0:
            raise Error ("No se puede sacar al azar un elemento de una lista vacía")
        max_posicion_elemento=len(lista)-1
        num_azar=randint(0, max_posicion_elemento)
        return lista[num_azar]