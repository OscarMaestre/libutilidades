class Documento(object):
    def __init__(self, nombre_archivo="documento.rst", fin_linea="\n", separador="\n\n"):
        self.nombre_archivo     =   nombre_archivo
        self.separador          =   separador
        self.fin_linea          =   fin_linea
        self.bloques            =   []
        self.subrayados         =   ["=", "-", "~"]

    def anadir_parrafo(self, parrafo):
        self.bloques.append(parrafo)


    def anadir_texto_con_linea_arriba_y_abajo(self, titulo, subrayador):
        self.bloques.append(self.get_texto_con_linea_arriba_y_abajo(titulo, subrayador))

    def get_texto_con_linea_arriba_y_abajo(self, titulo, subrayador):
        longitud_titulo=len(titulo)
        iguales=subrayador*longitud_titulo
        #Por este orden y de arriba a abajo
        # Signos igual --- separador --- titulo --separador ---igual---separador--separador
        plantilla="{0}{1}{2}{1}{0}{1}{1}"
        texto=plantilla.format(iguales,self.fin_linea,titulo)
        return texto
    

    def anadir_titulo(self, titulo):
        self.anadir_texto_con_linea_arriba_y_abajo(titulo, "=")
    
    def get_titulo(self, titulo):
        return self.get_texto_con_linea_arriba_y_abajo(titulo, "=")
    


    def anadir_subtitulo(self, subtitulo):
        self.anadir_texto_con_linea_arriba_y_abajo(subtitulo, "-")

    def get_subtitulo(self, subtitulo):
        self.get_texto_con_linea_arriba_y_abajo(subtitulo, "-")


    def anadir_lineas_numeradas(self, vector_lineas, con_numeracion=True, simbolo_alternativo="*"):
        self.bloques.append(self.get_lineas_numeradas(vector_lineas,con_numeracion, simbolo_alternativo))
    
    def get_lineas_numeradas(self, vector_lineas, con_numeracion=True, simbolo_alternativo="*"):
        nuevas_lineas=[]
        for pos, linea in enumerate(vector_lineas):
            inicio = str(pos)+"." if con_numeracion else simbolo_alternativo
            nueva_linea=inicio+" " +linea
            nuevas_lineas.append(nueva_linea)
        texto=self.fin_linea.join(nuevas_lineas)
        return texto

    def anadir_lineas_punteadas(self, vector_lineas):
        self.anadir_lineas_numeradas(vector_lineas, con_numeracion=False)
    
    def get_lineas_punteadas(self, vector_lineas):
        return self.get_lineas_numeradas(vector_lineas, con_numeracion=False)
    
    
    def anadir_lineas_con_guion(self, vector_lineas):
        self.anadir_lineas_numeradas(vector_lineas, con_numeracion=False, simbolo_alternativo="-")

    def get_lineas_con_guion(self, vector_lineas):
        self.get_lineas_numeradas(vector_lineas, con_numeracion=False, simbolo_alternativo="-")


    def anadir_titulo_de_nivel(self, titulo, nivel=1):
        self.bloques.append(self.get_titulo_de_nivel(titulo, nivel))

    def get_titulo_de_nivel(self, titulo, nivel=1):
        subrayador=self.subrayados[nivel-1]
        texto_subrayados=subrayador*len(titulo)
        #Estructura
        #Titulo--separador--subrayado
        plantilla="{0}{1}{2}"
        texto=plantilla.format(titulo, self.fin_linea, texto_subrayados)
        return texto


    def get_texto(self):
        texto=self.separador.join(self.bloques)
        return texto
    
    def guardar(self):
        with open (self.nombre_archivo) as fich:
            fich.write(texto)
        