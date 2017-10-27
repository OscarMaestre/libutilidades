#!/usr/bin/env python3
from urllib.parse import quote_plus
import requests

def get_latitud_longitud(localidad):
    localidad=quote_plus(localidad)
    if (localidad.find("orio de Illescas")!=-1):
        return (40.122994, -3.845876);
    print(localidad)
    prefijo="AIzaSyAxXzHSYNb1--uogBtoAgU3-yGnPG45qAA "
    url="https://maps.googleapis.com/maps/api/geocode/json?key={0}&address={1}+castilla+la+mancha".format(prefijo, localidad)
    
    peticion=requests.get(url)
    
    
    respuesta=peticion.json()
    print(respuesta)
    lat=respuesta['results'][0]['geometry']['location']['lat']
    longitud=respuesta['results'][0]['geometry']['location']['lng']
    return (lat, longitud)