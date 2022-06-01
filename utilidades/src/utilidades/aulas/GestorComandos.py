class GestorComandos(object):
    @staticmethod
    def set_ip(ip, mascara, gateway, nombre_tarjeta):
        PLANTILLA="netsh interface ip set address name= \"{3}\" static {0} {1} {2}"
        texto=PLANTILLA.format(ip, mascara, gateway, nombre_tarjeta)
        return texto
    
    @staticmethod
    def cambiar_dns(dns1, dns2, nombre_tarjeta):
        PLANTILLA_DNS="""
{0}
{1}
"""
        comando_dns_1="netsh interface ip set dns \"{0}\" static {1}" 
        comando_dns_2="netsh interface ip add dns \"{0}\" {1}"
        comando1=comando_dns_1.format(nombre_tarjeta, dns1)
        comando2=comando_dns_2.format(nombre_tarjeta, dns2)
        texto=PLANTILLA_DNS.format(comando1, comando2)
        return texto

    @staticmethod
    def cambiar_clave(usuario, nueva_clave):
        PLANTILLA_CAMBIO_CLAVE="net user {0} {1}"
        comando=PLANTILLA_CAMBIO_CLAVE.format(usuario, nueva_clave)
        return comando

    @staticmethod
    def cambiar_nombre(nuevo_nombre):
        PLANTILLA_CAMBIO_NOMBRE="""
        WMIC ComputerSystem where Name="%COMPUTERNAME%" call Rename Name="{0}"
        """
        comando=PLANTILLA_CAMBIO_NOMBRE.format(nuevo_nombre)
        return comando

    @staticmethod
    def unir_a_dominio():
        PLANTILLA_UNIR_DOMINIO="""
wmic computersystem where name="%computername%" call joindomainorworkgroup fjoinoptions=3 name="ciclos.local" username="admin" Password="inf-678"
        
        """
        return PLANTILLA_UNIR_DOMINIO


    @staticmethod
    def dar_propiedad_disco_a_alumno(usuario):
        PLANTILLA_PROPIEDAD="""
        ..\\..\\zenity.exe --file-selection --directory --title "Indica el disco del usuario {0}"
        """

        texto=PLANTILLA_PROPIEDAD.format(usuario)
        return texto

        