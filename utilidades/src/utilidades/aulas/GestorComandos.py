class GestorComandos(object):
    @staticmethod
    def set_ip(ip, mascara, gateway, nombre_tarjeta):
        PLANTILLA="netsh interface ip set address name= \"{3}\" static {0} {1} {2}"
        texto=PLANTILLA.format(ip, mascara, gateway, nombre_tarjeta)
        return texto
    
    @staticmethod
    def cambiar_dns(dns1, dns2, nombre_tarjeta):
        pass