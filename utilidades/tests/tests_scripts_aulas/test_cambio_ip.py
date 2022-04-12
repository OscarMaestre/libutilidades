#!/usr/bin/python3

from utilidades.aulas.CreadorScriptCambioIP import CreadorScriptCambioIP

CreadorScriptCambioIP.crear(
    "prueba.bat",
    "10.9.0.20", "255.255.0.0", "10.9.0.254", "Ethernet"
)