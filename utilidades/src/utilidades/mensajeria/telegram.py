#!/usr/bin/env python3
#coding=utf-8
import sys
if __name__ == '__main__':
    sys.exit()


import requests, json

from utilidades.modelos.Modelos import *

OFFSET_DEFECTO=-1

CLAVE_NOMBRE_CHAT='first_name'
ID_CHAT="id"
TIPO_CHAT="type"

CLAVE_NOMBRE_FROM='first_name'
CLAVE_ID_FROM="id"

CLAVE_CHAT="chat"
CLAVE_DATE="date"
CLAVE_FROM="from"
CLAVE_MESSAGE_ID="message_id"
CLAVE_MESSAGE="message"
CLAVE_UPDATE_ID="update_id"
CLAVE_TEXT="text"
CLAVE_OFFSET="offset"


TEXTO_ALTA="ALTA"
TEXTO_BAJA="BAJA"
TEXTO_ERROR_AFI="ERRORAFI"
TEXTO_ALTA_NO_AFILIADO="""
Lo sentimos, pero no hemos identificado tu DNI ({0}) como el de un afiliado de ANPE Ciudad Real.
Si nos hemos equivocado, por favor, llámanos al 926-27-41-41, escríbenos un email a afiliados@anpecr.com o
escribe un mensaje con el texto {1} y a continuación algunos datos (p.ej DNI, nombre y apellidos).
Si perteneces a otra provincia y deseas estar afiliado a ANPE Ciudad Real, por favor,
solicita el traslado en la sede de ANPE de tu provincia.
"""
TEXTO_ALTA_REALIZADA="""
Tu alta se ha realizado correctamente. Bienvenido al sistema de alertas al móvil de ANPE Ciudad Real.
Recuerda que puedes darte de baja enviando BAJA seguido de un espacio y seguido de tu DNI con letra.
"""
TEXTO_AYUDA="""
Hola, este es el sistema de alertas al móvil para los afiliados de ANPE Ciudad Real.
Si deseas darte de alta envia ALTA y tu DNI (recuerda incluir la letra) .
Si deseas darte de baja envia el texto BAJA y tu DNI (también con letra).
"""
RESULT="result"

class Chat(object):
    def __init__(self, objeto_json):
        self.first_name=objeto_json[CLAVE_NOMBRE_CHAT]
        self.id=objeto_json[ID_CHAT]
        self.type=objeto_json[TIPO_CHAT]
        
class From(object):
    def __init__(self, objeto_json):
        self.first_name=objeto_json[CLAVE_NOMBRE_FROM]
        self.id=objeto_json[CLAVE_ID_FROM]
        
class Message(object):
    def __init__(self, objeto_json):
        self.message_id=objeto_json[CLAVE_MESSAGE_ID]
        self.chat=Chat(objeto_json[CLAVE_CHAT])
        self.date=objeto_json[CLAVE_DATE]
        self.el_from=From ( objeto_json[CLAVE_FROM] )
        self.text=objeto_json[CLAVE_TEXT]
    
    def __str__(self):
        return "<Text: {0}>".format (self.text)
        
class Update(object):
    """Actualización recibida"""
    def __init__(self, objeto_json):
        self.update_id=objeto_json[CLAVE_UPDATE_ID]
        self.message=Message(objeto_json[CLAVE_MESSAGE])
    def es_alta(self):
        """
        Nos dice si un mensaje recibido es un alta o no.
        
        Devuelve
            (True, resto_mensaje) -- Si es un mensaje de alta
            
            (False, None) -- Si no es un mensaje de alta
        """
        texto_mensaje = self.message.text
        longitud_texto_alta = len( TEXTO_ALTA )
        subcadena= texto_mensaje[0:longitud_texto_alta]
        if subcadena==TEXTO_ALTA:
            return (True, texto_mensaje[longitud_texto_alta+1:] ) 
        return (False, None)
        
    def __str__(self):
        return "<id: {0}, {1}>".format ( self.update_id, str (self.message) )
    
class GestorTelegram(object):
    """Gestiona los mensajes de Telegram"""
    def __init__(self, token):
        self.token=token
        self.URL_BASE="https://api.telegram.org/bot"
    def getUpdates(self, offset=OFFSET_DEFECTO):
        """
        Descarga las actualizaciones en forma de una lista de objetos Update.
        
        Argumentos:
        
            offset -- Identificador del primer update_id. Debería ser el último recogido +1
        
        Devuelve
        
            Una lista de updates si todo va bien
            
            None si no funcionó
        """
        
        url=self.URL_BASE+self.token+"/getUpdates"
        if offset==OFFSET_DEFECTO:
            respuesta=requests.get ( url )
        else:
            diccionario=dict()
            diccionario[CLAVE_OFFSET]=offset
            respuesta=requests.get ( url, params=diccionario )
        objeto=json.loads(respuesta.text)
        if objeto['ok'] == True:
            updates=[]
            for u in objeto[RESULT]:
                objeto_update= Update (u)
                updates.append ( Update (u) )
            return updates
        else:
            print (objeto)
        return None
    def send_data_to_url(self, diccionario, url=None):
        if url==None:
            url_envio=self.URL_BASE+self.token+"/sendMessage"
        else:
            url_envio=url
        respuesta=requests.post(url_envio, diccionario)
        print (respuesta.text)
        
        
    def sendMessage(self, chat_id, text):
        """
        Envia un mensaje
        
        Parametros:
            
            chat_id -- id del chat al que enviar el texto
            
            text -- texto a enviar
        """
        diccionario_para_enviar_datos=dict()
        diccionario_para_enviar_datos['chat_id']=chat_id
        diccionario_para_enviar_datos['text']=text
        self.send_data_to_url(diccionario_para_enviar_datos)
    
    
    def dar_de_alta(self, chat_id, resto_texto):
        """ Da de alta a una persona """
        dni=resto_texto.strip()
        self.enviar_mensaje_ayuda ( chat_id, dni )
        
        
    def enviar_mensaje_ayuda ( self, chat_id, dni ):
        """Envia el mensaje de ayuda estándar"""
        return self.sendMessage ( chat_id, TEXTO_AYUDA.format ( dni, TEXTO_ERROR_AFI ) )
    
    def enviar_mensaje_alta_no_realizada( self, chat_id, dni ):
        """Envia el mensaje que indica que el alta no se ha hecho"""
        msg=TEXTO_ALTA_NO_AFILIADO.format ( dni, TEXTO_ERROR_AFI )
        print ("Enviando mensaje de ayuda")
        print ("-->"+msg)
        return self.sendMessage ( chat_id,  msg )
    
    def enviar_mensaje_alta_realizada( self, chat_id ):
        """Envia el mensaje que indica que el alta no se ha hecho"""
        return self.sendMessage ( chat_id,  TEXTO_ALTA_REALIZADA )
    
    def crear_base_datos_asociada(self, cad_conexion):
        motor= create_engine( cad_conexion , echo=False)
        creador_sesiones= sessionmaker(bind=motor)  
        sesion=creador_sesiones()