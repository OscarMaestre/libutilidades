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
        