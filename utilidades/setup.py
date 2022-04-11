#!/usr/bin/env python3
# coding=utf-8

#from distutils.core import setup
import os
from setuptools import setup


setup(name='utilidades',
      version='1.0',
      package_dir={'':'src'},
      packages=['utilidades',
                'utilidades.imagenes',
                'utilidades.aulas',
                'utilidades.documentos',
                'utilidades.email',
                'utilidades.fechas',
                'utilidades.excel',
                'utilidades.ficheros',
                'utilidades.genericas',
                'utilidades.modelos',
                'utilidades.mensajeria',
                'utilidades.basedatos',
                'utilidades.cadenas',
                'utilidades.internet',
                'utilidades.ip',
                'utilidades.vagrant',
                'utilidades.cisco'],

        #Si queremos incluir un fichero "estático" meterlo
        #en el Manifest.in
      include_package_data=True,
      #Indica aquí los paquetes que sean necesarios
      install_requires=[
          "ipaddress",
          "pytablewriter"
      ]
)

