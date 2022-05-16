class GestorNombres(object):
    def __init__(self, num_aula_sin_ceros, num_pc_sin_ceros) -> None:
        self.num_aula_sin_ceros = num_aula_sin_ceros
        self.num_pc_sin_ceros   = num_pc_sin_ceros
        self.num_aula_con_ceros = self.get_numero_con_ceros(self.num_aula_sin_ceros)
        self.num_pc_con_ceros   = self.get_numero_con_ceros(self.num_pc_sin_ceros)

        # Plantillas para los nombres de los equipos. 
        # En principio los equipos se llaman algo como AULAB09-PC04
        # Todo tiene dos digitos y si no los hay se rellena con 0, ejemplo PC04 o PC17
        self.PLANTILLA_NOMBRE_AULA="AULAB{0}"
        self.PLANTILLA_NOMBRE_PC="PC{0}"
        self.PLANTILLA_NOMBRE_COMPLETO_ORDENADOR="{0}-{1}"
        self.MAX_PC=20
        #Si hay otros ordenadores con otras IP poner aquí su último byte y su nombre
        #Por ejemplo, el PC con la IP xxx.xxx.xxx.100 suele ser el "PC-PROFESOR"
        self.OTROS_PC=[100, 101]
        self.NOMBRES_OTROS_PC=["PROFESOR", "BORRAR"]

    def get_numero_con_ceros(self, numero, cantidad_digitos_en_total=2):
        """Devuelve una cadena con el mismo número pero rellenada con ceros
        
                :param numero: numero a rellenar
                :param cantidad_digitos_en_total: cantidad de digitos que debe tener"""
        cadena=str(numero)
        cadena_con_ceros=cadena.zfill(cantidad_digitos_en_total)
        return cadena_con_ceros

    def get_nombre_aula(self):
        """Devuelve el nombre estándar del aula"""
        texto=self.PLANTILLA_NOMBRE_AULA.format(self.num_aula_con_ceros)
        return texto

    def get_nombre_pc(self):
        """Devuelve el nombre estándar del PC"""
        texto=self.PLANTILLA_NOMBRE_PC.format(self.num_pc_con_ceros)
        return texto

    def get_otros_nombres_equipo(self, num_pc):
        """Devuelve el nombre de un equipo usando la nomenclatura alternativa"""
        for pos, valor in enumerate(self.OTROS_PC):
            if valor==num_pc:
                return self.NOMBRES_OTROS_PC[pos]
        return "DESCONOCIDO"

    def get_nombre_completo_pc(self):
        """Devuelve el nombre del PC en formato AULABXX-PCXX"""
        #print(num_pc)
        if self.num_pc_sin_ceros>self.MAX_PC:
            nombre_pc=self.get_otros_nombres_equipo(self.num_pc_sin_ceros)
        else:
            nombre_pc=self.get_nombre_pc()
            
        nombre_aula=self.get_nombre_aula()
        
        texto=self.PLANTILLA_NOMBRE_COMPLETO_ORDENADOR.format(nombre_aula, nombre_pc)
        return texto
