#!/usr/bin/python3


from utilidades.documentos.Documento import Documento

lineas=["Soy una línea","Yo soy otra línea", "Y yo otra línea más muy larga"]

doc=Documento()
doc.anadir_titulo("Titulo del documento")

doc.anadir_subtitulo("Subtitulo del documento")
doc.anadir_parrafo("Soy un párrafo: Lorem Ipsum sidi hic amet")
doc.anadir_titulo_de_nivel("Soy un titulo de nivel 1", 1)

doc.anadir_lineas_numeradas(lineas)

doc.anadir_titulo_de_nivel("Soy un titulo de nivel 2", 2)
doc.anadir_lineas_punteadas(lineas)
doc.anadir_titulo_de_nivel("Soy un titulo de nivel 3", 3)
doc.anadir_lineas_con_guion(lineas)

cabeceras=["País", "Medallas", "Porcentaje"]
datos=[
    ["España", "7", "15%"],
    ["USA", "108", "35%"],
    ["China", "119", "45%"]
]
doc.anadir_tabla("Medallero", cabeceras, datos)

doc.anadir_figura("imagen.png", 75, "center", "Aqui va una imagen")
print(doc.get_texto())