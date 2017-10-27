#!/usr/bin/env python3
# coding=utf-8
#import smtplib
import email.encoders
from email.encoders import encode_base64
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import platform
import smtplib

class GestorEmail(object):
    def __init__(self):
        if platform.system()=="Linux":
            self.FICHERO_CONFIGURACION_EMAIL="/home/usuario/repos/configuracion_envio_email.txt"
            self.FICHERO_CONFIGURACION_EMAIL_AFILIADOS="/home/usuario/repos/configuracion_envio_email_afiliados.txt"
            self.FICHERO_DESTINATARIOS_EMAIL="/home/usuario/repos/destinatarios.txt"
        else:
            self.FICHERO_CONFIGURACION_EMAIL="C:\\repos\\configuracion_envio_email.txt"
            self.FICHERO_CONFIGURACION_EMAIL_AFILIADOS="C:\\repos\\configuracion_envio_email_afiliados.txt"
            self.FICHERO_DESTINATARIOS_EMAIL="C:\\repos\\destinatarios.txt"
            self.FICHERO_CONFIGURACION_EMAIL_LOCAL="C:\\repos\\configuracion_envio_email_oscar.txt"

    
    def enviar_email_sin_configuracion(self, remitente, destinatario,
                    asunto, mensaje, tupla_configuracion, ficheros):
        usuario         =   tupla_configuracion[0].strip()
        clave           =   tupla_configuracion[1].strip()
        servidor_smtp   =   tupla_configuracion[2].strip()
        puerto_smtp     =   tupla_configuracion[3].strip()
        servidor_pop    =   tupla_configuracion[4].strip()
        puerto_pop      =   tupla_configuracion[5].strip()
        
        msg = MIMEMultipart()
        part = MIMEText('text', "html", _charset="utf-8")
        msg['Subject'] = asunto
        msg['To'] = destinatario
        msg['From'] = remitente
        print ("Enviando email desde {0} a {1}".format(usuario, destinatario))
        files = ficheros
        for filename in files:
            fich=open(filename, "rb")
    
            adjunto=MIMEBase("application", "octet-stream")
            adjunto.set_payload(fich.read(), charset="utf-8")
            fich.close()
            encode_base64(adjunto)
            adjunto.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(adjunto)
    
        part.set_payload(mensaje, charset="UTF-8")
        msg.attach(part)
    
        session = smtplib.SMTP(servidor_smtp, puerto_smtp)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(usuario, clave)
        session.sendmail(remitente, destinatario, msg.as_string())
        session.quit()
    #La configuración del remitente debe estar en un fichero
    #La primera línea es la dirección del servidor de correo como por ejemplo pepito@gmail.com
    #La segunda contiene la clave
    #La tercera linea es el servidor de correo SMTP
    #La cuarta contiene el numero de puerto
    def get_parametros(self, fichero_configuracion_remitente):
        with open(fichero_configuracion_remitente) as f:
            lineas=f.readlines()
        
        usuario         =   lineas[0].strip()
        clave           =   lineas[1].strip()
        servidor_smtp   =   lineas[2].strip()
        puerto_smtp     =   lineas[3].strip()
        servidor_pop    =   lineas[4].strip()
        puerto_pop      =   lineas[5].strip()
        try:
            nombre_remitente=lineas[6].strip()
        except :
            nombre_remitente=usuario
            print("****************************************************************************")
            print ("No hay un nombre de remitente en la linea 7 de "+fichero_configuracion_remitente)
            print ("Usando el usuario como remitente (en este caso se usará {0})".format(usuario))
            print("****************************************************************************")
            
        return (usuario, clave, servidor_smtp, puerto_smtp, servidor_pop, puerto_pop, nombre_remitente)

    def enviar_email(self, remitente, destinatario, asunto, mensaje, fichero_configuracion_email, ficheros):
        (usuario, clave, servidor_smtp, puerto_smtp, servidor_pop, puerto_pop, remitente)=self.get_parametros(fichero_configuracion_email)
        msg = MIMEMultipart()
        part = MIMEText('text', "html", _charset="utf-8")
        msg['Subject'] = asunto
        msg['To'] = destinatario
        msg['From'] = remitente
        print ("Enviando email desde {0} a {1}".format(usuario, destinatario))
        files = ficheros
        for filename in files:
            fich=open(filename, "rb")
    
            adjunto=MIMEBase("application", "octet-stream")
            adjunto.set_payload(fich.read(), charset="utf-8")
            fich.close()
            encode_base64(adjunto)
            adjunto.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(adjunto)
    
        part.set_payload(mensaje, charset="UTF-8")
        msg.attach(part)
    
        session = smtplib.SMTP(servidor_smtp, puerto_smtp)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(usuario, clave)
        session.sendmail(remitente, destinatario, msg.as_string())
        session.quit()

    def enviar_email_servicio_automatico(self, asunto, mensaje, lista_destinatarios):
        for destinatario in lista_destinatarios:
            self.enviar_email("servicioemailautomatico@gmail.com",
                         destinatario, asunto, mensaje, FICHERO_CONFIGURACION_EMAIL, [])
    def enviar_email_servicio_corporativo(self, asunto, mensaje, lista_destinatarios):
        for destinatario in lista_destinatarios:
            self.enviar_email("servicioemailautomatico@gmail.com",
                         destinatario, asunto, mensaje, FICHERO_CONFIGURACION_EMAIL_LOCAL, [])

    def enviar_matriculas_cursos(self, mensaje, lista_ficheros):
        (usuario, clave,
         servidor_smtp, puerto_smtp,
         servidor_pop, puerto_pop,remitente)=self.get_parametros(self.FICHERO_CONFIGURACION_EMAIL_LOCAL)
        self.enviar_email(remitente, "oscar@anpecr.com", "Matriculas cursos", mensaje, self.FICHERO_CONFIGURACION_EMAIL_LOCAL, lista_ficheros)
        self.enviar_email(remitente, "formacion@anpeclm.com", "Matriculas cursos", mensaje, self.FICHERO_CONFIGURACION_EMAIL_LOCAL, lista_ficheros)
        
