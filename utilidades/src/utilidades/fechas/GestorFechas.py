#!/usr/bin/env python3
# coding=utf-8
import datetime
from datetime import timedelta
class GestorFechas(object):
    def convertir_fecha_a_formato_iso(self, fecha):
        posibles_separadores=["-", "/"]
        separador=""
        for sep in posibles_separadores:
            if fecha.find(sep)!=-1:
                separador=sep
                break
        trozos=fecha.split(sep)
        dia=trozos[0]
        mes=trozos[1]
        anio=trozos[2]
        return "{0}-{1}-{2}".format ( anio, mes, dia )
    
    def convertir_fecha_de_iso_a_estandar(self, fecha):
        posibles_separadores=["-", "/"]
        separador=""
        for sep in posibles_separadores:
            if fecha.find(sep)!=-1:
                separador=sep
                break
        trozos=fecha.split(sep)
        anio=trozos[0]
        mes=trozos[1]
        dia=trozos[2]
        return "{0}-{1}-{2}".format ( dia, mes, anio )
    
    def get_hoy_iso(self):
        hoy=datetime.datetime.now()
        return hoy.strftime("%Y-%m-%d")
    
    def get_hoy_espanol(self):
        hoy=datetime.datetime.now()
        return hoy.strftime("%d-%m-%Y")
    
    def get_rango_fechas_ultima_semana(self):
        hoy=datetime.datetime.now()
        diferencia=datetime.timedelta(days=7)
        hace_una_semana=hoy-diferencia
        return (hace_una_semana, hoy)