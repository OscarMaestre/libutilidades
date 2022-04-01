#!/usr/bin/python3

from utilidades.imagenes.CreadorImagenes import CreadorImagenes
import utilidades.imagenes
from importlib.resources import contents, open_binary

origen="imagentransparente.png"
destino="destino.png"

c=CreadorImagenes(origen, destino)

lista_fuentes=c.get_lista_posibles_fuentes()
print(lista_fuentes)

#Probamos un solo texto
c.poner_texto("Hola mundo, esto es un texto de prueba", 100, 100)

#Probamos varias textos en varias coordenadas
tuplas=[ (100, 200) , (150, 80), (0, 20)]
textos=[]
for t in tuplas:
    textos.append("Estoy en ({0},{1})".format(t[0], t[1]))

c.poner_textos(textos, tuplas)
c.guardar()
