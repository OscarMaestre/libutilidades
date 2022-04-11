import pytablewriter

class Documento(object):
    def __init__(self, nombre_archivo="documento.rst", fin_linea="\n", separador="\n\n"):
        self.nombre_archivo     =   nombre_archivo
        self.separador          =   separador
        self.fin_linea          =   fin_linea
        self.bloques            =   []
        self.subrayados         =   ["=", "-", "~"]

    def anadir_parrafo(self, parrafo):
        """
        Anade un párrafo al documento
        """
        self.bloques.append(parrafo)


    def anadir_texto_con_linea_arriba_y_abajo(self, titulo, subrayador):
        """Añade al documento un texto con el subrayador especificado
            Parametros: 
                titulo: texto del titulo
                subrayador: símbolo para crear las líneas"""
        self.bloques.append(self.get_texto_con_linea_arriba_y_abajo(titulo, subrayador))

    def get_texto_con_linea_arriba_y_abajo(self, titulo, subrayador):
        """Genera un texto con una linea de simbolos arriba y abajo
        
            Parametros: 
                titulo: texto del titulo
                subrayador: símbolo para crear las líneas"""
        longitud_titulo=len(titulo)
        iguales=subrayador*longitud_titulo
        #Por este orden y de arriba a abajo
        # Signos igual --- separador --- titulo --separador ---igual---separador--separador
        plantilla="{0}{1}{2}{1}{0}{1}{1}"
        texto=plantilla.format(iguales,self.fin_linea,titulo)
        return texto
    

    def anadir_titulo(self, titulo):
        """Añade el título del documento"""
        self.anadir_texto_con_linea_arriba_y_abajo(titulo, "=")
    
    def get_titulo(self, titulo):
        """Genera el titulo de un documento"""
        return self.get_texto_con_linea_arriba_y_abajo(titulo, "=")
    


    def anadir_subtitulo(self, subtitulo):
        """Anade el subtítulo del documento"""
        self.anadir_texto_con_linea_arriba_y_abajo(subtitulo, "-")

    def get_subtitulo(self, subtitulo):
        """Genera el subtítulo de un documento"""
        self.get_texto_con_linea_arriba_y_abajo(subtitulo, "-")


    def anadir_lineas_numeradas(self, vector_lineas, con_numeracion=True, simbolo_alternativo="*"):
        """Genera una lista numerada
        
            Parametros:
                vector_lineas: lista con las lineas a añadir
                con_numeracion: Indica si vamos a usar numeros o no
                simbolo_alternativo: Indica el simbolo que vamos a poner delante"""
        self.bloques.append(self.get_lineas_numeradas(vector_lineas,con_numeracion, simbolo_alternativo))
    
    def get_lineas_numeradas(self, vector_lineas, con_numeracion=True, simbolo_alternativo="*"):
        """Genera líneas numeradas
        
            Parametros:
                vector_lineas: lista de lineas a numerar
                con_numeracion: indica si usaremos numeros o no
                simbolo_alternativo: SI NO ESTAMOS NUMERANDO se pondrá este símbolo delante"""
        nuevas_lineas=[]
        for pos, linea in enumerate(vector_lineas):
            inicio = str(pos)+"." if con_numeracion else simbolo_alternativo
            nueva_linea=inicio+" " +linea
            nuevas_lineas.append(nueva_linea)
        texto=self.fin_linea.join(nuevas_lineas)
        return texto

    def anadir_lineas_punteadas(self, vector_lineas):
        """Genera una lista punteada
        
            Parametros:
                vector_lineas: lista de lineas se van a añadir"""
        self.anadir_lineas_numeradas(vector_lineas, con_numeracion=False)
    
    def get_lineas_punteadas(self, vector_lineas):
        """Genera una lista punteada con el asterisco:
        
            Parametros: 
                vector_lineas: lista de lineas a puntear"""
        return self.get_lineas_numeradas(vector_lineas, con_numeracion=False)
    
    
    def anadir_lineas_con_guion(self, vector_lineas):
        """Genera una lista punteada con guiones
        
            Parametros:
                vector_lineas: lista de lineas a añadir."""
        self.anadir_lineas_numeradas(vector_lineas, con_numeracion=False, simbolo_alternativo="-")

    def get_lineas_con_guion(self, vector_lineas):
        """Devuelve una lista de líneas con el guión delante
        
            Parametros:
                vector_lineas: lista de lineas"""
        self.get_lineas_numeradas(vector_lineas, con_numeracion=False, simbolo_alternativo="-")


    def anadir_titulo_de_nivel(self, texto_titulo, nivel=1):
        """Añade un título de nivel 1, 2, o 3
        
            Parametros:
                titulo: texto del titulo
                nivel: nivel de titulo a generar"""
        self.bloques.append(self.get_titulo_de_nivel(texto_titulo, nivel))

    def get_titulo_de_nivel(self, texto_titulo, nivel=1):
        """Genera un título del nivel pedido
        
            Parametros:
                texto_titulo: Texto del título
                nivel: nivel del título pedido (1,2 o 3)"""
        subrayador=self.subrayados[nivel-1]
        texto_subrayados=subrayador*len(texto_titulo)
        #Estructura
        #Titulo--separador--subrayado
        plantilla="{0}{1}{2}"
        texto=plantilla.format(texto_titulo, self.fin_linea, texto_subrayados)
        return texto

    def anadir_tabla(self, nombre_tabla, lista_cabeceras, lista_de_listas_con_datos):
        """Añade una tabla en formato RestructuredText

            Parameters:
                nombre_tabla: nombre con el que la tabla aparece en el documento
                lista_cabeceras: lista de textos que aparecerán en las cabeceras de la tabla
                lista_de_lista_con_datos:lista de listas en las que aparecen las filas de datos
        """
        texto=self.get_tabla(nombre_tabla, lista_cabeceras, lista_de_listas_con_datos)
        self.anadir_parrafo(texto)

    def get_tabla(self, nombre_tabla, lista_cabeceras, lista_de_listas_con_datos):
        """Devuelve una tabla en formato RestructuredText

            Parameters:
                nombre_tabla: nombre con el que la tabla aparece en el documento
                lista_cabeceras: lista de textos que aparecerán en las cabeceras de la tabla
                lista_de_lista_con_datos:lista de listas en las que aparecen las filas de datos
        """
        writer = pytablewriter.RstGridTableWriter(
        headers=lista_cabeceras,
        value_matrix=lista_de_listas_con_datos,
        table_name=nombre_tabla
        )
        return writer.dumps()
        
    def get_texto(self):
        """Recuperar el texto del documento"""
        texto=self.separador.join(self.bloques)
        return texto

    def anadir_figura(self, ruta_imagen, porcentaje_escalado=100, alineacion="center", texto_alternativo=""):
        """Anade una figura para restructuredtext o Sphinx
        
            Parametros:
                ruta_imagen: ruta a un archivo de imagen.
                porcentaje_escalado: número entero que indica el tamaño a escalar.
                alineacion: puede ser "left", "right" o "center"
                texto_alternativo: Si no se puede ver la imagen en el navegador se mostrará este texto"""
        bloque=self.get_figura(ruta_imagen, porcentaje_escalado, alineacion, texto_alternativo)
        self.anadir_parrafo(bloque)
    
    def get_figura(self, ruta_imagen, porcentaje_escalado=100, alineacion="center", texto_alternativo=""):
        """Genera una figura para restructuredtext o Sphinx
        
            Parametros:
                ruta_imagen: ruta a un archivo de imagen.
                porcentaje_escalado: número entero que indica el tamaño a escalar.
                alineacion: puede ser "left", "right" o "center"
                texto_alternativo: Si no se puede ver la imagen en el navegador se mostrará este texto"""
        PLANTILLA_FIGURA="""
.. figure:: {0}
   :scale: {1}%
   :align: {2}
   :alt: {3}

   {3}

"""
        texto=PLANTILLA_FIGURA.format(ruta_imagen, porcentaje_escalado, alineacion, texto_alternativo)
        return texto


    def anadir_bloque_codigo(self, programa, lenguaje):
        """Añade un bloque de código
        
            Parámetros:
                programa: texto del programa
                lenguaje: lenguaje en el que está escrito"""
        PLANTILLA="""
.. code-block:: {0}

{1}
"""
        texto_tabulado=self.tabular_texto(programa)
        texto_final=PLANTILLA.format(lenguaje, texto_tabulado)
        self.anadir_parrafo(texto_final)

    def anadir_literal(self, texto):
        """Añade un texto literal"""
        nuevo_texto=self.tabular_texto(texto)
        self.anadir_parrafo(nuevo_texto)

    def tabular_texto(self, texto):
        """Pone un tabular al principio de cada línea del texto"""
        lineas=texto.split("\n")
        nuevas_lineas=[]
        for linea in lineas:
            nueva_linea="\t"+linea
            nuevas_lineas.append(nueva_linea)
        nuevo_texto="\n".join(nuevas_lineas)
        return nuevo_texto

    def guardar(self, codificacion="utf-8"):
        with open (self.nombre_archivo, "w", encoding=codificacion) as fich:
            fich.write(self.get_texto())
        