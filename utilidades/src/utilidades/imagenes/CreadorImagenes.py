from PIL import Image, ImageDraw, ImageFont

from importlib.resources import contents, open_binary, path
from glob import glob
import utilidades.imagenes.fuentes
import inspect
import os

class CreadorImagenes(object):
    def __init__(self, archivo_imagen, archivo_resultado, tamano_fuente=18, paquete_fuente="utilidades.imagenes.fuentes.cantarell", archivo_fuente="Cantarell-Regular.ttf") -> None:
        """Constructor

            :param archivo_imagen: ruta del archivo de imagen donde vamos a escribir
            :param archivo_resultado: ruta del archivo donde se va a dejar el resultado.
            :param tamano_fuente: tamaño de la fuente
            :param paquete_fuente: paquete de donde se va a cargar la fuente
            :param archivo_fuente: archivo de fuente TTF con el que se va  escribir 
        """
        self.imagen=Image.open(archivo_imagen).convert("RGBA")
        self.paquete_fuente=paquete_fuente
        self.archivo_fuente=archivo_fuente
        self.bytes_fichero=open_binary(paquete_fuente, archivo_fuente)
        self.tamano_fuente=tamano_fuente
        self.font= ImageFont.truetype(self.bytes_fichero, tamano_fuente)
        self.contexto=ImageDraw.Draw(self.imagen)
        self.archivo_resultado=archivo_resultado    

    def get_lista_posibles_fuentes(self):
        """Devuelve una lista con las posibles fuentes que se pueden usar"""
        fuentes=[]
        directorios_con_fuentes=["cantarell", "liberation-mono", "linux-biolinum", "nimbus-roman-no9-l","nimbus-sans-l","oxygen"]
        for d in directorios_con_fuentes:
            ruta_paquete="utilidades.imagenes.fuentes."+d
            ruta=os.path.dirname(inspect.getfile(utilidades.imagenes.fuentes))
            subdir=os.path.join(ruta, d, "*.ttf")
            ficheros_ttf=glob(subdir, recursive=True)
            for f in ficheros_ttf:
                ruta_relativa=os.path.basename(f)
                fuentes.append((ruta_paquete, ruta_relativa))
            
            subdir=os.path.join(ruta, d, "*.otf")
            ficheros_ttf=glob(subdir, recursive=True)
            for f in ficheros_ttf:
                ruta_relativa=os.path.basename(f)
                fuentes.append((ruta_paquete, ruta_relativa))
            
        return fuentes
    
    def set_fuente(self, ruta_paquete, nombre_archivo_ttf_u_otf):
        """Cambia la fuente activa
        
            :param ruta_paquete: ruta del paquete en forma de nombres separados por puntos (ej utilidades.imagenes.fuentes)
            :param nombre_archivo_ttf_u_otf: nombre del archivo de tipo de letra en formato TTF u OTF
        """
        bytes_fichero=open_binary(ruta_paquete, nombre_archivo_ttf_u_otf)
        self.font= ImageFont.truetype(bytes_fichero)
    

        
    def poner_texto(self, texto, x, y, color=(0, 0, 0)):
        """Inserta un texto en la imagen.
        
                :param texto:  texto a insertar
                :param x,y: coordenadas
                :param color: color en formato (R, G, B)
        """
        self.contexto.text( (x, y), text=texto, font=self.font, fill=color)
        

    def poner_textos(self, lista_textos, lista_tuplas_xy, color=(0,0,0)):
        """Inserta un conjunto de textos en las coordenadas correspondientes

                :param lista_textos: una lista de cadenas
                :param lista_tuplas_xy: una lista de tuplas con coordenadas (x,y)
        """
        for tupla in zip(lista_textos, lista_tuplas_xy):
            texto=tupla[0]
            tupla_xy=tupla[1]
            self.poner_texto(texto, tupla_xy[0], tupla_xy[1], color)
            
    def get_resultado(self):
        self.imagen.save(self.archivo_resultado)
    
    def guardar(self):
        """Guarda la imagen generada"""
        self.get_resultado()