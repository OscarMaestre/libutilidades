#!/usr/bin/env python3
# coding=utf-8

import sqlite3
import os
import platform
import tempfile
from .ConstantesBaseDatosSQLite import *


class GestorBD(object):
    
    def __init__(self, archivo_db):
        self.debug=False
        self.archivo_db=archivo_db
        self.conexion=sqlite3.connect(self.archivo_db)
        self.cursor=self.conexion.cursor()
        self.ejecutar_sentencias(["PRAGMA foreign_keys=ON"])

    @staticmethod        
    def get_preludio_sql(nombre_funcion):
        return PRELUDIO_SQL.format(nombre_funcion)

    @staticmethod
    def crear_sentencia_update(sentencia):
        sql="\tsql=\""+sentencia+"\"\n"
        sql+="\tdb.Execute sql, dbFailOnError\n"
        return sql
    
    def crear_tabla_itinerancias(self, nombre_tabla=NOMBRE_TABLA_ITINERANCIAS):
        self.ejecutar_sentencias(
            [
                SQL_CREACION_PLANTILLAS.format ( nombre_tabla )
            ]
        )
    @staticmethod
    def get_procedimiento(nombre, sql_intermedio):
        inicio=GestorBD.get_preludio_sql(nombre)
        fin=GestorBD.get_fin_sql()
        return inicio+sql_intermedio+fin
    @staticmethod
    def get_fin_sql():
        return FIN_SQL_ACCESS
    
    def activar_depuracion(self):
        self.debug=True
        
    def desactivar_depuracion(self):
        self.debug=False
        
    def get_unico_valor(self, sql_con_valor_unico):
        if self.debug:
            print (sql_con_valor_unico)
        filas=self.get_filas(sql_con_valor_unico)
        #print(filas)
        return filas[0][0]
    
    def ejecutar_sentencias(self, lista_sentencias):
        for sql in lista_sentencias:
            if self.debug:
                print("-"*20)
                print (sql)
                print("-"*20)
            try:
                self.cursor.execute(sql)
            except:
                print("Fallo la sentencia siguiente:")
                print(sql)
        self.conexion.commit()
    
    def get_filas(self, select):
        filas=self.cursor.execute(select)
        return filas.fetchall()
    def cuantos_cumplen_select(self, select):
        filas=self.get_filas(select)
        return len(filas)
    def __del__(self):
        self.cursor.close()
        
    def get_descripcion(self):
        return self.cursor.description
    def get_nombres_columnas(self):
        descripciones=self.cursor.description
        nombres_columnas=[]
        for d in descripciones:
            nombres_columnas.append ( d[0] )
        return nombres_columnas
            
    def extraer_tuplas_especialidades_de_fichero(self, nombre_fichero):
        fichero=open(nombre_fichero, encoding="utf-8")
        lineas=fichero.readlines()
        tuplas=[]
        for l in lineas:
            codigo=l[0:3]
            descripcion=l[4:].strip()
            tuplas.append( ( codigo, descripcion ) )
        fichero.close()
        return tuplas
    
    def crear_tabla_todas_especialidades(self, nombre_tabla_especialidades):
        sql=SQL_CREACION_ESPECIALIDADES.format(nombre_tabla_especialidades)
        
        self.ejecutar_sentencias([sql])
        ficheros=["590", "591", "592", "594", "595", "596", "597"]
        for f in ficheros:
            self.crear_tabla_especialidades(f, nombre_tabla_especialidades)
            
            
    def crear_tabla_especialidades(self, codigo_cuerpo, nombre_tabla_especialidades):
        f=codigo_cuerpo
        sql=[]
        dir_actual=os.path.dirname(os.path.realpath(__file__))
        ruta_fichero=dir_actual+os.path.sep+"Especialidades0{0}.txt".format(f)
        especialidades=self.extraer_tuplas_especialidades_de_fichero( ruta_fichero )
        for tupla in especialidades:
            codigo=tupla[0]
            nombre=tupla[1]
            #                                                  Codigo    Nombre Idioma   ¿tiempo parcial?
            insert="insert or ignore into especialidades values ('0{2}{0}', '{1}', 'ESPAÑOL', 'NO')".format(codigo, nombre, f)
            sql.append(insert)
            #                                                  Codigo    Nombre Idioma   ¿tiempo parcial?
            insert="insert or ignore into especialidades values ('P{2}{0}', '{1}', 'ESPAÑOL', 'SI')".format(codigo, nombre, f)
            sql.append(insert)
            #                                                  Codigo    Nombre Idioma   ¿tiempo parcial?
            insert="insert or ignore into especialidades values ('B{2}{0}', '{1}', 'INGLÉS', 'NO')".format(codigo, nombre, f)
            sql.append(insert)
            #                                                  Codigo    Nombre Idioma   ¿tiempo parcial?
            insert="insert or ignore into especialidades values ('W{2}{0}', '{1}', 'INGLÉS', 'SI')".format(codigo, nombre, f)
            sql.append(insert)
            #                                                  Codigo    Nombre Idioma   ¿tiempo parcial?
            insert="insert or ignore into especialidades values ('R{2}{0}', '{1}', 'FRANCÉS', 'SI')".format(codigo, nombre, f)
            sql.append(insert)
            #                                                  Codigo    Nombre Idioma   ¿tiempo parcial?
            insert="insert or ignore into especialidades values ('F{2}{0}', '{1}', 'FRANCÉS', 'NO')".format(codigo, nombre, f)
            sql.append(insert)
        self.ejecutar_sentencias(sql)
        
    def get_sql_especialidades(self):
        sql=[]
        insert_primaria="insert or ignore into especialidades values ('PRIMARIA', 'DESCONOCIDA', 'ESPAÑOL', 'NO')"
        sql.append(insert_primaria)
        insert_secundaria="insert or ignore into especialidades values ('SECUNDARIA', 'DESCONOCIDA', 'ESPAÑOL', 'NO')"
        sql.append(insert_secundaria)
        ficheros=["590", "591", "592", "594", "595", "596", "597"]
        for f in ficheros:
            self.crear_tabla_especialidades(f, "especialidades")
        return sql
    
    def crear_tablas_iniciales_en_bd(self):
        self.ejecutar_sentencias(["PRAGMA foreign_keys=ON"])
        self.ejecutar_sentencias(["PRAGMA foreign_keys=ON"])
        self.crear_tabla_todas_especialidades("especialidades")
        self.ejecutar_sentencias([ SQL_CREACION_NOMBRAMIENTOS ])
        self.ejecutar_sentencias ( BD_RESULTADOS.get_sql_especialidades() )
        
    def cambiar_nombres_por_codigos(self, nombre_tabla_rutas, nombre_tabla_localidades):
        sql_localidades="select nombre_localidad from {0}".format ( nombre_tabla_localidades )
        if self.debug:
            print (sql_localidades)
        filas_localidades=self.get_filas ( sql_localidades )
        sql_extractor_codigo="select codigo_localidad from {0} where nombre_localidad='{1}'"
        sentencias_update=[]
        for localidad in filas_localidades:
            codigo_localidad=self.get_unico_valor ( sql_extractor_codigo.format(
                nombre_tabla_localidades, localidad[0]
            ), 'codigo_localidad')
            sql_update="update {0} set origen='{1}' where origen='{2}'".format (
                nombre_tabla_rutas, codigo_localidad, localidad[0]
            )
            sentencias_update.append(sql_update)
            sql_update="update {0} set destino='{1}' where destino='{2}'".format (
                nombre_tabla_rutas, codigo_localidad, localidad[0]
            )
            sentencias_update.append(sql_update)
            
        excepciones=[
            ("130360002", "Cortijos de Arriba"),
            ("130360002", "Cortijo de Arriba"),
        ]
        for tupla in excepciones:
            codigo_localidad=tupla[0]
            localidad=tupla[1]
            sql_update="update {0} set origen='{1}' where origen='{2}'".format (
                nombre_tabla_rutas, codigo_localidad, localidad
            )
            sentencias_update.append(sql_update)
            sql_update="update {0} set destino='{1}' where destino='{2}'".format (
                nombre_tabla_rutas, codigo_localidad, localidad
            )
            sentencias_update.append(sql_update)
        
        self.ejecutar_sentencias(sentencias_update)
