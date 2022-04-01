from PIL import Image, ImageDraw, ImageFont


class CreadorImagenes(object):
    def __init__(self, archivo_imagen, archivo_resultado, archivo_fuente) -> None:
        self.imagen=Image.open(archivo_imagen).convert("RGBA")
        self.font= ImageFont.truetype(archivo_fuente, 40)
        self.contexto=ImageDraw.Draw(self.imagen)
        self.archivo_resultado=archivo_resultado    

    def poner_texto(self, texto, x, y, color=(0, 0, 0)):
        """Inserta un texto en la imagen.
        
            Argumentos:
            
            texto:  texto a insertar
            x,y : coordenadas
        """
        self.contexto.text( (x, y), text=texto, font=self.font, fill=color)
        
    def get_resultado(self):
        self.imagen.save(self.archivo_resultado)
    
    def guardar(self):
        """Guarda la imagen generada"""
        self.get_resultado()