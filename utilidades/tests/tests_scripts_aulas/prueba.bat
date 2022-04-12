
        
@cls
@echo ************************************************************
@echo              Cambio de la direccion IP
@echo ************************************************************
        

        
@echo.

@echo.
@echo.
@echo NUEVOS DATOS IP-->Tarjeta:'Ethernet', IP:10.9.0.20 / 255.255.0.0, Puerta enlace:10.9.0.254
@echo.
@echo.
    
@pause


        netsh interface ip set address name= "Ethernet" static 10.9.0.20 255.255.0.0 10.9.0.254

        
@echo.

@echo.
@echo.
@echo Comprueba si ha habido algún error conocido. Si no es así, pulsa una tecla para acabar.
@echo.
@echo.
    
@pause

        