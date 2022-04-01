from PIL import Image, ImageDraw, ImageFont

from importlib.resources import contents, open_binary, path
from glob import glob
import utilidades.imagenes.fuentes
import inspect
import os

class CreadorImagenes(object):
    def __init__(self, archivo_imagen, archivo_resultado, tamano_fuente=18, paquete_fuente="utilidades.imagenes.fuentes.cantarell", archivo_fuente="Cantarell-Regular.ttf") -> None:
        self.imagen=Image.open(archivo_imagen).convert("RGBA")
        self.paquete_fuente=paquete_fuente
        self.archivo_fuente=archivo_fuente
        self.bytes_fichero=open_binary(paquete_fuente, archivo_fuente)
        self.tamano_fuente=tamano_fuente
        self.font= ImageFont.truetype(self.bytes_fichero, tamano_fuente)
        self.contexto=ImageDraw.Draw(self.imagen)
        self.archivo_resultado=archivo_resultado    

    def get_lista_posibles_fuentes(self):
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
        bytes_fichero=open_binary(ruta_paquete, nombre_archivo_ttf_u_otf)
        self.font= ImageFont.truetype(bytes_fichero)
    

        
    def poner_texto(self, texto, x, y, color=(0, 0, 0)):
        """Inserta un texto en la imagen.
        
            Argumentos:
            
            texto:  texto a insertar
            x,y : coordenadas
        """
        self.contexto.text( (x, y), text=texto, font=self.font, fill=color)
        

    def poner_textos(self, lista_textos, lista_tuplas_xy, color=(0,0,0)):
        """Inserta un conjunto de textos en las coordenadas correspondientes

            Argumentos:

                lista_textos: una lista de cadenas
                lista_tuplas_xy: una lista de tuplas con coordenadas (x,y)
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