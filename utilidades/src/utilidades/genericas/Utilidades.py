from random import randint
import telegram_send
from bs4 import BeautifulSoup

class Utilidades(object):

    @staticmethod
    def anadir_tabuladores(texto, num_tabs=1):
        """

        Dado un texto añade tabuladores a todos los comienzos de línea

        Argumentos:

            texto -- Texto a tabular

            num_tabs -- Cantidad de tabuladores a añadir al principio

        """
        lineas=texto.split('\n')
        prefijo = "\t"*num_tabs
        lineas_con_tab=[prefijo+linea for linea in lineas]
        return "\n".join(lineas_con_tab)

    @staticmethod
    def embellecer_xml(cadena_xml):
        """
        
        Dada una cadena XML embellece el resultado y
        lo alinea
        
        Argumentos:
        
            cadena_xml -- Cadena a embellecer
        """
        sopa=BeautifulSoup(cadena_xml, 'xml')
        embellecido=sopa.prettify()
        
        return embellecido

    @staticmethod
    def embellecer_html(cadena_html):
        """
        
        Dada una cadena HTML embellece el resultado y
        lo alinea
        
        Argumentos:
        
            cadena_xml -- Cadena a embellecer
        """
        sopa=BeautifulSoup(cadena_html, 'html.parser')
        embellecido=sopa.prettify()
        
        return embellecido

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