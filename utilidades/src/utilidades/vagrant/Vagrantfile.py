#!/usr/bin/python3


from dataclasses import dataclass

FICHERO_PLANTILLA="""
Vagrant.configure("2") do |config|
{0}
end
"""

BLOQUE_RAM="""
    config.vm.provider "virtualbox" do |vb|
        vb.gui = true
        vb.memory = "{0}"
    end
"""

PROVISIONADO="""
    config.vm.provision "shell", inline: <<-SHELL
{0}
    SHELL
"""

class PuertoAbierto(object):
    def __init__(self, puerto_invitado, puerto_anfitrion, ip_invitado=None, ip_anfitrion=None) -> None:
        self.puerto_invitado    =   puerto_invitado
        self.puerto_anfitrion   =   puerto_anfitrion
        self.ip_invitado        =   ip_invitado
        self.ip_anfitrion       =   ip_anfitrion
    def __str__(self) -> str:
        lista=[]
        trozo1="guest: \"{0}\"".format(self.puerto_invitado)
        lista.append(trozo1)
        trozo2="host: \"{0}\"".format(self.puerto_anfitrion)
        lista.append(trozo2)
        if self.ip_anfitrion!=None:
            trozo3="host_ip: \"{0}\"".format(self.ip_anfitrion)
            lista.append(trozo3)
        if self.ip_invitado!=None:
            trozo4="guest_ip: \"{0}\"".format(self.ip_invitado)
            lista.append(trozo4)
        parametros=", ".join(lista)
        linea="    config.vm.network \"forwarded_port\", {0}".format(parametros)
        return linea
        

class FicheroParaCopiar(object):
    def __init__(self, fichero_en_anfitrion, fichero_en_invitado) -> None:
        self.fichero_en_anfitrion=fichero_en_anfitrion
        self.fichero_en_invitado=fichero_en_invitado
    def __str__(self) -> str:
        plantilla="    config.vm.provision \"file\", source: \"{0}\", destination: \"{1}\""
        texto=plantilla.format(self.fichero_en_anfitrion, self.fichero_en_invitado)
        return texto



class Vagrantfile(object):
    def __init__(self):
        self.MEGAS_RAM      =   768
        self.maquina_base   =   "oscarmaestre/ubuntuserver20"
        self.bloques        =   []
        self.puertos_abiertos=  []
        self.num_tarjetas_puente=0
        
        self.carpeta_compartida_invitado=None
        self.carpeta_compartida_anfitrion=None

        self.ficheros_para_copiar=[]
        self.comandos=[]
        self.nombre_tarjeta_puente=None

    def abrir_puerto(self, puerto_en_anfitrion, puerto_en_invitado, ip_invitado=None, ip_anfitrion=None):
        """
        Abre un puerto en el host anfitrión:
            :param puerto_en_anfitrión: puerto en el que va a escuchar el anfitrión.
            :param puerto_en_invitado: puerto al que se va a redirigir la conexión cuando llegue.
            :param ip_invitado: dirección IP del invitado que va a escuchar.
            :param ip_anfitrión: dirección IP del anfitrión.
        """
        puerto=PuertoAbierto(puerto_en_invitado, puerto_en_anfitrion, ip_invitado, ip_anfitrion)
        self.puertos_abiertos.append(puerto)
        
    def anadir_comando(self, comando):
        """
        Añadir un comando que se ejecutará cuando se inyecte la máquina virtual.

            :param comando: Comando a añadir.
        """
        self.comandos.append(comando)

    def anadir_tarjeta_puente(self, nombre_tarjeta):
        """
        Añadir una tarjeta en modo puente.

            :param nombre_tarjeta: nombre que recibe EN EL ANFITRIÓN la tarjeta con la cual se va a conectar la tarjeta puente que añadamos. En Linux será algo como enp0s3 y en Windows algo como Ethernet
        """
        self.num_tarjetas_puente=self.num_tarjetas_puente+1
        self.nombre_tarjeta_puente=nombre_tarjeta

    def anadir_carpeta_compartida(self, carpeta_en_anfitrion, carpeta_en_invitado):
        """
        Añadir una carpeta compartida.

            :param carpeta_en_anfitrion: ruta de la carpeta en el anfitrión.
            :param carpeta_en_invitado: ruta de la carpeta en el invitado. En Linux pondremos algo como /compartida y en Windows algo como H:
        """
        self.carpeta_compartida_anfitrion=carpeta_en_anfitrion
        self.carpeta_compartida_invitado=carpeta_en_invitado

    def anadir_fichero_para_copiar(self, ruta_en_anfitrion, ruta_en_invitado):
        """
        Añadir un fichero que se copiará dentro del invitado, puede ser una carpeta.

            :param ruta_en_anfitrion: ruta de la carpeta o fichero en el anfitrión.
            :param ruta_en_invitado: ruta de la carpeta o fichero donde aparecerá DENTRO del invitado.
        """
        fichero=FicheroParaCopiar(ruta_en_anfitrion, ruta_en_invitado)
        self.ficheros_para_copiar.append(fichero)

    def get_carpetas_compartidas(self):
        """
        DE USO INTERNO. Devuelve las carpetas compartidas listas para meter
        en el Vagrantfile
        """
        if self.carpeta_compartida_anfitrion==None:
            return ""
        plantilla="    config.vm.synced_folder \"{0}\", \"{1}\""
        texto=plantilla.format(self.carpeta_compartida_anfitrion, self.carpeta_compartida_invitado)
        return texto

    def get_ficheros_para_copiar(self):
        """
        DE USO INTERNO. Devuelve los ficheros a copiar listos para meter
        en el Vagrantfile
        """
        if self.ficheros_para_copiar==[]:
            return ""
        lineas=[str(fichero) for fichero in self.ficheros_para_copiar]
        return "\n".join(lineas)

    def get_tarjetas_puente(self):
        """
        DE USO INTERNO. Devuelve las tarjetas puente listas para meter
        en el Vagrantfile
        """
        configuracion=["    config.vm.network \"public_network\", bridge: \"{0}\"".format(self.nombre_tarjeta_puente)]
        lineas=self.num_tarjetas_puente * configuracion
        return "\n".join(lineas)

    def get_puertos(self):
        """
        DE USO INTERNO. Devuelve los puertos abiertos listos para meter
        en el Vagrantfile
        """
        if self.puertos_abiertos==[]:
            return ""
        lineas_puertos=[str(puerto) for puerto in self.puertos_abiertos]
        return "\n".join(lineas_puertos)

    def set_maquina_base(self, maquina_base):
        """
        Establece el nombre de la máquina base.

            :param maquina_base: ruta de la máquina base. Puede ser algo como oscarmaestre/ubuntuserver20 o una ruta completa como M:\boxes\maquina.box
        """
        self.maquina_base=maquina_base

    def set_megas_ram(self, megas_ram):
        """
        Establece la cantida de RAM de la máquina en megas.

            :param megas_ram: Cantidad de RAM en megas
        """
        self.MEGAS_RAM=megas_ram

    def get_maquina_base(self):
        """
        DE USO INTERNO. Devuelve el nombre de la máquina base para meter
        en el Vagrantfile
        """
        plantilla="    config.vm.box = \"{0}\""
        texto=plantilla.format(self.maquina_base)
        return texto

    def get_comandos(self):
        """
        DE USO INTERNO. Devuelve los comandos a ejecutar listos para meter
        en el Vagrantfile
        """
        if self.comandos==[]:
            return ""
        lineas=["        "+comando for comando in self.comandos]
        comandos="\n".join(lineas)
        provisionado=PROVISIONADO.format(comandos)
        return provisionado

    def get_texto_vagrantfile(self):
        """
        DE USO INTERNO. Devuelve el texto que irá en el fichero Vagrantfile
        """
        bloques=[]

        bloques.append(self.get_maquina_base())
        bloques.append(BLOQUE_RAM.format(self.MEGAS_RAM))
        bloques.append(self.get_puertos())
        bloques.append(self.get_tarjetas_puente())
        bloques.append(self.get_carpetas_compartidas())
        bloques.append(self.get_ficheros_para_copiar())
        bloques.append(self.get_comandos())
        texto="\n".join(bloques)
        vagrantfile_texto=FICHERO_PLANTILLA.format(texto)
        return vagrantfile_texto

    def guardar_como(self, ruta_archivo):
        """
        Guarda el fichero Vagrantfile

            :param ruta_archivo: ruta completa donde se guardará el archivo
        """
        with open(ruta_archivo, "w") as fich:
            fich.write(self.get_texto_vagrantfile())