import yaml

class NetplanGenerator(object):
    """Generador de configuraciones para netplan"""
    def __init__(self) -> None:
        self.config_dict=dict()
        self.cards=dict()
        self.activate_ethernets=False

    def add_wired_network_card_with_dhcp(self, cardname):
        """Añade una tarjeta de red cableada que debe obtener su IP por DHCP
        
            Argumentos:
            
                cardname -- Nombre de la tarjeta: enp0s3, enp0s8...
        """
        self.activate_ethernets=True
        config=dict()
        config["dhcp4"]="true"
        self.cards[cardname]=config

    def _get_gw_routes(self, default_gw_array):
        """Método privado
        
            Argumentos:
            
                default_gw_array: lista de gateways por defecto
                
            Devuelve:
            
                Una lista de diccionarios con to y default lista para ser añadida a netplan
                
        """
        gws=[]
        for gw in default_gw_array:
            gw_dict=dict()
            gw_dict["to"]="default"
            gw_dict["via"]=gw
            gws.append(gw_dict)
        return gws
    
    def add_wired_network_card_with_ip(self, cardname, ips_array, default_gw_array):
        """Añade una tarjeta de red cableada con IP estática
        
            Argumentos:
            
                cardname: Nombre de la tarjeta de red, enp0s3, enp0s8...
                ips_array: IP estática en formato 192.168.1.10/24
                default_gw_array: Array de gateways por defecto
        """
        self.activate_ethernets=True
        config=dict()
        config["dhcp4"]="false"
        config["addresses"]=ips_array
        if default_gw_array!=[]:
            gws=self._get_gw_routes(default_gw_array)
            config["routes"]=gws
        self.cards[cardname]=config
        
        
    
        
    def get_str_with_tabs(self, prefix_char="\t", num_of_prefix_chars=1):
        aux=str(self)        
        lines=aux.split("\n")
        tabs=prefix_char*num_of_prefix_chars
        lines_with_tabs=[f"{tabs}{line}" for line in lines]
        return "\n".join(lines_with_tabs)
    
    def __str__(self) -> str:
        self.config_parameters=dict()
        self.config_parameters["version"]=2
        self.config_parameters["renderer"]="NetworkManager"

        if self.activate_ethernets:
            dict_ethernets=dict()
            for k, v in enumerate(self.cards):
                dict_ethernets[v]=self.cards[v]
            self.config_parameters["ethernets"]=dict_ethernets
        
        result=dict()
        result["network"]=self.config_parameters
        aux=yaml.dump(result)
        return aux

if __name__=="__main__":
    n=NetplanGenerator()
    n.add_wired_network_card_with_dhcp("enp0s3")
    n.add_wired_network_card_with_dhcp("enp0s8")
    n.add_wired_network_card_with_ip("enp0s7", ["192.168.1.10/24"], ["192.168.1.1"])
    print(n)

        

