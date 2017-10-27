#!/usr/bin/env python3
#coding=utf-8


import re
INICIO_NO_ENCONTRADO=-1
DECIMAL_NO_ENCONTRADO=-2
PATRON_NO_ENCONTRADO="PATRON_NO_ENCONTRADO"

re_cifras_en_plantillas="(\-|[0-9]+)"
re_cifras_unidades="[0-9]+"
expr_regular_cifras_en_plantillas=re.compile(re_cifras_en_plantillas)
expr_regular_cifras_unidades=re.compile(re_cifras_unidades)

def corregir_vi(nombre_localidad):
    temp=nombre_localidad
    temp=temp.replace("VI", "Vi")
    return temp

def corregir_articulo(pueblo):
    pueblo=pueblo.strip()
    articulos=[" (El)", " (La)", " (Los)", " (Las)"]
    corregido=["El", "La", "Los", "Las"]
    
    for pos in range(0, len(articulos)):
        if pueblo.find(articulos[pos])!=-1:
            pueblo=pueblo.replace(articulos[pos], "")
            pueblo=corregido[pos]+" " + pueblo
            return pueblo
    return pueblo

def corregir_nombre_localidad(pueblo):
    pueblo=corregir_vi(pueblo)
    pueblo=corregir_articulo(pueblo)
    return pueblo

def quitar_pueblo_entre_parentesis(cadena):
    pos_parentesis=cadena.find("(")
    if pos_parentesis!=-1:
        return cadena[:pos_parentesis-1]
    return cadena

def extraer_patron(exp_regular_compilada, linea):
    concordancia=exp_regular_compilada.search(linea)
    if concordancia:
        inicio=concordancia.start()
        final=concordancia.end()
        patron=concordancia.string[inicio:final]
        return (inicio, final, patron)
    return (INICIO_NO_ENCONTRADO, INICIO_NO_ENCONTRADO, PATRON_NO_ENCONTRADO)


def extraer_cifras_plantillas(linea):
    concordancia=expr_regular_cifras_en_plantillas.search(linea)
    if concordancia:
        cifras=expr_regular_cifras_en_plantillas.findall(linea)
        lista_cifras=[]
        for c in cifras:
            if (c=='-'):
                lista_cifras.append(0)
            else:
                lista_cifras.append(int(c))
        return lista_cifras
    return (DECIMAL_NO_ENCONTRADO, DECIMAL_NO_ENCONTRADO, PATRON_NO_ENCONTRADO)

def extraer_cifras_unidades(linea):
    concordancia=expr_regular_cifras_unidades.search(linea)
    if concordancia:
        cifras=expr_regular_cifras_unidades.findall(linea)
        lista_cifras=[]
        for c in cifras:
            if (c=='-'):
                lista_cifras.append(0)
            else:
                lista_cifras.append(int(c))
        return lista_cifras
    return (DECIMAL_NO_ENCONTRADO, DECIMAL_NO_ENCONTRADO, PATRON_NO_ENCONTRADO)