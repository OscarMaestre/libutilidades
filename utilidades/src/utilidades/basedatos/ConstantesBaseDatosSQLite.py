#!/usr/bin/env python3
# coding=utf-8

import sys
if __name__ == '__main__':
    sys.exit()
    
import platform
CODIGOS_PROVINCIAS=[    ("02", "ALBACETE"),     ("13", "CIUDAD REAL"),
                        ("16", "CUENCA"),       ("19", "GUADALAJARA"),
                        ("45", "TOLEDO")]

SQL_CREACION_NOMBRAMIENTOS="""
CREATE TABLE if not exists nombramientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nif character(12),
    nombre_completo character(160),
    codigo_centro character(14),
    procedimiento character(40),
    fecha_procedimiento date not null, 
    fecha_inicio character(20),
    fecha_fin character(20),
    especialidad character(150),
    auxiliar character(2048),
    foreign key (especialidad) references especialidades(especialidad)
);
"""

SQL_CREACION_ESPECIALIDADES="""

create table if not exists {0}(
    especialidad character(150) primary key,
    descripcion character(250),
    idioma character(30),
    tiempo_parcial character(20)
);
"""

NOMBRE_TABLA_ITINERANCIAS="itinerancias"
SQL_CREACION_ITINERANCIAS="""
CREATE TABLE if not exists {0} (
    codigo_especialidad 	char(150),
    codigo_centro_origen	char(10),
    codigo_centro_destino	char(10),
    anio			int,
    foreign key (codigo_especialidad) references especialidades(especialidad),
    foreign key (codigo_centro_origen) references especialidades(centros_region),
    foreign key (codigo_centro_destino) references especialidades(centros_region)
)
""".format ( NOMBRE_TABLA_ITINERANCIAS )

NOMBRE_TABLA_PLANTILLAS="plantillas"
SQL_CREACION_PLANTILLAS="""
CREATE TABLE if not exists {0} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anio integer,
    codigo_centro char(10),
    codigo_especialidad char(150),
    tipo_plaza char(20),
    cantidad integer,
    foreign key (codigo_especialidad) references especialidades(especialidad)
    );
"""

if (platform.system()=="Linux"):
    ARCHIVO_RESULTADOS="/home/usuario/repos/varios/pruebas_proceso/nombramientos.db"
if (platform.system()=="Windows"):
    ARCHIVO_RESULTADOS="C:\\repos\\pruebas_proceso\\nombramientos.db"

PRELUDIO_SQL="Public Function {0} ()"
	
PRELUDIO_SQL+="""

On Error Resume Next

  Dim ws As Workspace
  Dim db As Database
  Dim strSQL As String

  Set ws = DBEngine.Workspaces(0)
  Set db = ws.Databases(0)

On Error GoTo Proc_Err
  'Todas las actualizaciones se meten en una transaccion
  ws.BeginTrans
"""

FIN_SQL_ACCESS="""
		 'se hace el commit
  ws.CommitTrans

Proc_Exit:
  Set ws = Nothing
  Set db = Nothing
  Exit Function

Proc_Err:
  ws.Rollback
  MsgBox "Error actualizando: " & Err.Description
  Resume Proc_Exit
End Function
	"""

NOMBRE_TABLA_ESPECIALIDADES="especialidades"
NOMBRE_TABLA_PARTICIPANTES="participantes"
NOMBRE_TABLA_ERRORES="errores"
SQL_CREACION_PARTICIPANTES="""
create table if not exists {0} (
    nif character(12) ,
    nombre_completo character(160),
    primary key (nif)
)
"""

NOMBRE_TABLA_ESPECIALIDADES_PARTICIPANTES="especialidades_participantes"

SQL_CREACION_ESPECIALIDADES_PARTICIPANTES="""
create table if not exists {0} (
    nif character(12),
    anio_participacion unsigned int,
    anio_oposicion unsigned int,
    nota_oposicion float,
    especialidad char(10),
    foreign key (nif) references {1}(nif),
    foreign key (especialidad) references {2}(especialidad)
)
"""
SQL_CREACION_ERRORES="""
create table if not exists {0} (
    id integer primary key autoincrement,
    nif character(12),
    anio_baremo unsigned int,
    apartado char(10),
    descripcion char(2048),
    perjudicial char(10),
    foreign key (nif) references {1}(nif)
)
"""

NOMBRE_TABLA_RESULTAS="resultas"
SQL_CREACION_RESULTAS="""
create table if not exists {0} (
    nif character(12),
    anio_participacion unsigned int,
    codigo_centro char(10),
    especialidad char(10),
    primary key (nif, especialidad),
    foreign key (nif) references {1}(nif),
    foreign key (especialidad) references {2}(especialidad)
)
"""


NOMBRE_TABLA_PUNTUACION="puntuacion"
SQL_CREACION_PUNTUACION="""
create table if not exists {0} (
    nif character(12),
    anio_participacion unsigned int,
    especialidad char(10),
    tipo_baremo char(15),
    {1}
    ,foreign key (nif) references {2}(nif)
)
"""


NOMBRE_TABLA_DERECHO_PREF_CENTRO="dpc"
SQL_CREACION_DPC="""
create table if not exists {0} (
    nif character(12),
    anio_participacion unsigned int,
    especialidad char(10),
    tipo_baremo char(15),
    codigo_centro char(10),
    foreign key (codigo_centro) references {1} (codigo_centro),
    foreign key (nif) references {2}(nif)
)
"""

NOMBRE_TABLA_DERECHO_PREF_CENTRO="dplz"
SQL_CREACION_DPLZ="""
create table if not exists {0} (
    nif character(12),
    anio_participacion unsigned int,
    especialidad char(10),
    tipo_baremo char(15),
    codigo_localidad char(10),
    foreign key (codigo_localidad) references {1} (codigo_localidad),
    foreign key (nif) references {2}(nif)
)
"""
