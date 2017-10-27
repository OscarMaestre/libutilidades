#!/usr/bin/env python3
# coding=utf-8

import sys

import utilidades
import utilidades.email

from utilidades.fechas.GestorFechas import GestorFechas
from utilidades.excel.GestorExcel import EscritorExcel
gf=GestorFechas()
fecha_iso="2016-01-21"

fecha_estandar=gf.convertir_fecha_de_iso_a_estandar(fecha_iso)
print ("{0} transformado en {1}".format ( fecha_iso, fecha_estandar ))

from  utilidades.email.GestorEmail import GestorEmail

gm=GestorEmail()
