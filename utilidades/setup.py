#!/usr/bin/env python3
# coding=utf-8

#from distutils.core import setup
import os
from setuptools import setup
ficheros_especialidades=[]
ficheros_especialidades.append ( os.sep.join(["utilidades","modelos","Especialidades0597.txt"]))
#print (ficheros_especialidades)
setup(name='utilidades',
      version='1.0',
      package_dir={'':'src'},
      packages=['utilidades',
                'utilidades.email',
                'utilidades.fechas',
                'utilidades.excel',
                'utilidades.ficheros',
                'utilidades.modelos',
                'utilidades.mensajeria',
                'utilidades.basedatos',
                'utilidades.cadenas',
                'utilidades.internet'],
      package_data={'utilidades.modelos':ficheros_especialidades},
      include_package_data=True
)