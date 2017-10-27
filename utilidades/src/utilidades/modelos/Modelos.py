#!/usr/bin/env python3
#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()
from sqlalchemy import Column, Integer, String, Boolean

NOMBRE_TABLA_CRUCE_INTERINOS_BOLSAS="interinos_bolsas"
NOMBRE_TABLA_INTERINOS="interinos"
NOMBRE_TABLA_BOLSAS="bolsas"
NOMBRE_TABLA_GASEOSA="gaseosa"
NOMBRE_TABLA_CORRESPONDENCIAS="correspondencias"
NOMBRE_TABLA_ESPECIALIDADES="especialidades"
NOMBRE_TABLA_ULTIMAS_BOLSAS="ultima_relacion_bolsa"
NOMBRE_TABLA_GRUPOS_MENSAJERIA="grupos_mensajeria"
NOMBRE_TABLA_MIEMBRO_GRUPO="miembro_grupo"
NOMBRE_TABLA_PERTENENCIA_GRUPO="miembro_pertenece_grupo"
NOMBRE_TABLA_MENSAJES_EN_COLA="mensajes_en_cola"
NOMBRE_TABLA_ULTIMAS_ACTUALIZACIONES="ultimas_actualizaciones"
BOLSA_597_CONVOCADAS=1
BOLSA_597_NO_CONVOCADAS=BOLSA_597_CONVOCADAS+1
MAX_LONGITUD_DESCRIPCION_ESPECIALIDAD=100
MAX_LONGITUD_DNI=10
MAX_LONGITUD_TLF=20
MAX_LONGITUD_NOMBRE=100



class Gaseosa(Base):
    __tablename__=NOMBRE_TABLA_GASEOSA
    dni=Column(String(10), primary_key=True)
    
class Especialidad(Base):
    __tablename__=NOMBRE_TABLA_ESPECIALIDADES
    codigo_especialidad=Column(String, primary_key=True)
    descripcion=Column(String(MAX_LONGITUD_DESCRIPCION_ESPECIALIDAD) )
    con_ingles=Column (Boolean, default=False, unique=False)
    con_frances=Column (Boolean, default=False, unique=False)
    a_tiempo_parcial=Column (Boolean, default=False, unique=False)
    
    @staticmethod
    def extraer_tuplas_especialidades_de_fichero(nombre_fichero):
        fichero=open(nombre_fichero, encoding="utf-8")
        lineas=fichero.readlines()
        tuplas=[]
        for l in lineas:
            codigo=l[0:3]
            descripcion=l[4:].strip()
            tuplas.append( ( codigo, descripcion ) )
        fichero.close()
        return tuplas
    
    @staticmethod
    def crear_todas_especialidades(sesion, codigo_cuerpo, crear_bolsas_asociadas=False):
        f=codigo_cuerpo
        sql=[]
        dir_actual=os.path.dirname(os.path.realpath(__file__))
        ruta_fichero=dir_actual+os.path.sep+"Especialidades0{0}.txt".format(f)
        especialidades=Especialidad.extraer_tuplas_especialidades_de_fichero( ruta_fichero )
        lista_especialidades_a_insertar=[]
        for tupla in especialidades:
            codigo_especialidad_extraida=tupla[0]
            nombre=tupla[1]
            exige_bilingue_ingles=True
            no_exige_bilingue_ingles=False
            exige_bilingue_frances=True
            no_exige_bilingue_frances=False
            es_a_tiempo_parcial=True
            no_es_a_tiempo_parcial=False
            #Creamos todas las especialidades con todas las combinaciones
            #de ingles y frances
            
            #0590107 es 0(Tiempo completo, sin bilingüismo) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="0"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                con_ingles=no_exige_bilingue_ingles,
                con_frances=no_exige_bilingue_frances,
                a_tiempo_parcial=no_es_a_tiempo_parcial)
            lista_especialidades_a_insertar.append ( especialidad )
            
            #P590107 es P(Tiempo completo, sin bilingüismo) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="P"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                con_ingles=no_exige_bilingue_ingles,
                con_frances=no_exige_bilingue_frances,
                a_tiempo_parcial=es_a_tiempo_parcial)
            lista_especialidades_a_insertar.append ( especialidad )
            
            #B590107 es B(Tiempo completo, bilingüe inglés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="B"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                con_ingles=exige_bilingue_ingles,
                con_frances=no_exige_bilingue_frances,
                a_tiempo_parcial=no_es_a_tiempo_parcial)
            lista_especialidades_a_insertar.append ( especialidad )
            
            #W590107 es W(Tiempo parcial, bilingüe inglés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="W"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                con_ingles=exige_bilingue_ingles,
                con_frances=no_exige_bilingue_frances,
                a_tiempo_parcial=es_a_tiempo_parcial)
            lista_especialidades_a_insertar.append ( especialidad )
            
            #R590107 es R(Tiempo completo, bilingüe francés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="R"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                con_ingles=no_exige_bilingue_ingles,
                con_frances=exige_bilingue_frances,
                a_tiempo_parcial=es_a_tiempo_parcial)
            lista_especialidades_a_insertar.append ( especialidad )
            
            #F590107 es F(Tiempo completo, bilingüe francés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="F"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                con_ingles=no_exige_bilingue_ingles,
                con_frances=exige_bilingue_frances,
                a_tiempo_parcial=no_es_a_tiempo_parcial)
            lista_especialidades_a_insertar.append ( especialidad )
            
        sesion.add_all ( lista_especialidades_a_insertar )
        sesion.commit()

def get_directorio_archivos_especialidades():
    dir_instalacion=os.path.dirname(os.path.realpath(__file__) )
    return dir_instalacion
def extraer_tuplas_especialidades_de_fichero(nombre_fichero):
        fichero=open(nombre_fichero, encoding="utf-8")
        lineas=fichero.readlines()
        tuplas=[]
        for l in lineas:
            codigo=l[0:3]
            descripcion=l[4:].strip()
            tuplas.append( ( codigo, descripcion ) )
        fichero.close()
        return tuplas

class Correspondencia(Base):
     __tablename__ = NOMBRE_TABLA_CORRESPONDENCIAS
     codigo_gaseosa=Column(Integer, primary_key=True)
     codigo_real=Column(String,
            ForeignKey(NOMBRE_TABLA_ESPECIALIDADES+".codigo_especialidad"),
            primary_key=True)
    
class Interino(Base):
     __tablename__ = NOMBRE_TABLA_INTERINOS

     dni = Column(String(MAX_LONGITUD_DNI), primary_key=True)
     nombre= Column(String(MAX_LONGITUD_NOMBRE))
     bilingue_ingles=Column(Boolean, default=False, unique=False)
     bilingue_frances=Column(Boolean, default=False, unique=False)
     disponible=Column(Boolean, default=True, unique=False)
     def __repr__(self):
        return "<Interino (nombre='%s', dni='%s', frances=%s, ingles=%s)>" % (
                             self.nombre, self.dni, self.bilingue_frances, self.bilingue_ingles)
    
    
class InterinosBolsas(Base):
    __tablename__=NOMBRE_TABLA_CRUCE_INTERINOS_BOLSAS
    
    dni_interino=Column (String(MAX_LONGITUD_DNI), ForeignKey(NOMBRE_TABLA_INTERINOS+".dni"), primary_key=True)
    
    codigo_especialidad=Column(String,
                               ForeignKey (
                                NOMBRE_TABLA_ESPECIALIDADES+".codigo_especialidad"
                                ), primary_key=True
                        )
    numero_en_bolsa=Column ( Integer, unique=False )
    
    def __str__(self):
        return "Dni:{0} en {1}".format ( self.dni_interino, self.codigo_especialidad)
    
class UltimaRelacionInterinosBolsas(Base):
    __tablename__=NOMBRE_TABLA_ULTIMAS_BOLSAS
    dni_interino=Column (String(MAX_LONGITUD_DNI), ForeignKey(NOMBRE_TABLA_CRUCE_INTERINOS_BOLSAS+".dni_interino"), primary_key=True)
    
    codigo_especialidad=Column(String,
                               ForeignKey (
                                NOMBRE_TABLA_ESPECIALIDADES+".codigo_especialidad"
                                ), primary_key=True
                        )
    num_orden=Column ( Integer, unique=False )
    
class GrupoMensajeria(Base):
    __tablename__=NOMBRE_TABLA_GRUPOS_MENSAJERIA
    id=Column(Integer, primary_key=True, nullable=False)
    nombre=Column ( String(MAX_LONGITUD_NOMBRE))
    
class MiembroGrupo(Base):
    __tablename__=NOMBRE_TABLA_MIEMBRO_GRUPO
    id=Column(Integer, primary_key=True, nullable=False)
    nombre=Column ( String(MAX_LONGITUD_NOMBRE))
    numero_movil = Column ( String (MAX_LONGITUD_TLF ) )
    
class MiembroPerteneceGrupo(Base):
    __tablename__=NOMBRE_TABLA_PERTENENCIA_GRUPO
    id_miembro=Column(Integer,
                      ForeignKey(NOMBRE_TABLA_MIEMBRO_GRUPO+".id"),
                      primary_key=True, nullable=False)
    id_grupo=Column(Integer,
                      ForeignKey(NOMBRE_TABLA_GRUPOS_MENSAJERIA+".id"),
                      primary_key=True, nullable=False)

class MensajeEnCola(Base):
    __tablename__=NOMBRE_TABLA_MENSAJES_EN_COLA
    id=Column(Integer, primary_key=True, nullable=False)
    numero_movil = Column ( String (MAX_LONGITUD_TLF ) )
    enviado_correctamente=Column(Boolean, default=False, unique=False)
    
class UltimaActualizacion(Base):
    __tablename__=NOMBRE_TABLA_ULTIMAS_ACTUALIZACIONES
    id=Column(Integer, primary_key=True, nullable=False)
    
    