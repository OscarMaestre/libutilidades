#!/usr/bin/python3

from utilidades.vagrant.Vagrantfile import Vagrantile
gestor_vagrant=Vagrantile()
gestor_vagrant.abrir_puerto(8080, 80, "10.0.2.15", "192.168.1.100")
gestor_vagrant.anadir_tarjeta_puente("enp0s25")
gestor_vagrant.anadir_tarjeta_puente("enp0s25")
gestor_vagrant.anadir_carpeta_compartida("en_anfitrion", "/invitado")
gestor_vagrant.anadir_fichero_para_copiar("anfitrion.txt", "en_invitado.txt")
gestor_vagrant.anadir_comando("apt-get update -y")
gestor_vagrant.anadir_comando("apt-get upgrade -y")
gestor_vagrant.anadir_comando("apt-get install apache2 -y")

texto=gestor_vagrant.get_texto_vagrantfile()

print(texto)

#gestor_vagrant.guardar_como("borrame")