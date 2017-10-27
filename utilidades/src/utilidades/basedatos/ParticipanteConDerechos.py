#!/usr/bin/env python3
# coding=utf-8

from .ListaCampos import ListaCampos

class ParticipanteConDPC(object):
    def __init__(self, dni, anio_participacion, tipo_baremo, cod_centro):
        self.dni=dni
        self.anio_participacion=anio_participacion
        self.tipo_baremo=tipo_baremo
        self.codigo_centro=cod_centro
        
    
    def generar_sql_insert(self):
        lista_campos=ListaCampos()
        lista_campos.anadir ("nif", self.dni )
        lista_campos.anadir ( "anio_participacion", self.anio_participacion, ListaCampos.NUMERO)
        lista_campos.anadir ( "tipo_baremo", self.tipo_baremo )
        lista_campos.anadir ( "codigo_centro", self.codigo_centro)
        sql_parcial=lista_campos.generar_insert("dpc")
        return sql_parcial


class ParticipanteConDPLZ(object):
    def __init__(self, dni, anio_participacion, tipo_baremo, codigo_localidad):
        self.dni=dni
        self.anio_participacion=anio_participacion
        self.tipo_baremo=tipo_baremo
        self.codigo_localidad=codigo_localidad
        
    
    def generar_sql_insert(self):
        lista_campos=ListaCampos()
        lista_campos.anadir ("nif", self.dni )
        lista_campos.anadir ( "anio_participacion", self.anio_participacion, ListaCampos.NUMERO)
        lista_campos.anadir ( "tipo_baremo", self.tipo_baremo )
        lista_campos.anadir ( "codigo_localidad", self.codigo_localidad)
        sql_parcial=lista_campos.generar_insert("dplz")
        return sql_parcial

