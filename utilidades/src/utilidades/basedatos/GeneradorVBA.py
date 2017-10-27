#!/usr/bin/env python3
#coding=utf-8
from utilidades.ficheros.GestorFicheros import GestorFicheros

class GeneradorVBA(object):
    @staticmethod
    def get_preludio_sql(nombre_funcion):
        preludio_sql="Public Function "+nombre_funcion+"()"
        
        preludio_sql+="""
    
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
        return preludio_sql
    
    
    @staticmethod
    def crear_sentencia_update(sentencia):
        sql="\tstrSQL=\""+sentencia+"\"\n"
        sql+="\tdb.Execute strSQL, dbFailOnError\n"
        return sql
        
    @staticmethod
    def get_sql_update(nombre_tabla, campo_a_actualizar, valor_a_escribir,
                       campo_condicion,valor_campo_condicion):
        cad_sql="update {0} set {1}='{2}' where {3}='{4}'";
        resultado=cad_sql.format (
            nombre_tabla, campo_a_actualizar, valor_a_escribir,
            campo_condicion, valor_campo_condicion
        )
        return resultado
        
    @staticmethod
    def get_procedimiento(nombre, sql_intermedio):
        inicio=get_preludio_sql(nombre)
        fin=get_fin_sql()
        return inicio+sql_intermedio+fin
    
    @staticmethod    
    def get_fin_sql():
        sql="""
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
        return sql
    
    @staticmethod
    def generar_funcion (vector_tuplas, nombre_funcion, nombre_tabla,
                           nombre_campo_actualizar, nombre_campo_condicion,
                           nombre_campo_auxiliar=None):
        vba=GeneradorVBA.get_preludio_sql(nombre_funcion)
        for t in vector_tuplas:
            valor_a_escribir=t[0]
            valor_campo_condicion=t[1]
            sentencia_update=GeneradorVBA.get_sql_update(nombre_tabla, nombre_campo_actualizar, valor_a_escribir,
                       nombre_campo_condicion,valor_campo_condicion)
            vba+=GeneradorVBA.crear_sentencia_update(sentencia_update)
            if nombre_campo_auxiliar!=None:
                valor_campo_auxiliar=t[2]
                sentencia_update=GeneradorVBA.get_sql_update(nombre_tabla,
                        nombre_campo_auxiliar, valor_campo_auxiliar,
                       nombre_campo_condicion,valor_campo_condicion)
                vba+=GeneradorVBA.crear_sentencia_update(sentencia_update)
                
        vba+=GeneradorVBA.get_fin_sql()
        return vba
    
    @staticmethod
    def generar_modulo_vba(vector_tuplas, nombre_tabla,
                           nombre_campo_actualizar, nombre_campo_condicion,
                           nombre_modulo, campo_auxiliar=None):
        gf=GestorFicheros()
        vba=""
        prefijo_funcion="f_{0}"
        funcion_global="\r\nPublic Function f_global()\r\n{0}\r\nEnd Function"
        funcion_parcial="Public Function {0}(){1}\r\nEnd Function"
        max=100 #Se generan funciones con este maximo de sentencias
        contador=0
        num_funcion=1
        vba_parcial=""
        funciones=[]
        while len(vector_tuplas)!=0:
            trozo=vector_tuplas[0:max]
            nombre_funcion="f_"+str(num_funcion)
            vba_parcial+=GeneradorVBA.generar_funcion (trozo, nombre_funcion,
                nombre_tabla,nombre_campo_actualizar, nombre_campo_condicion, campo_auxiliar)
            vector_tuplas=vector_tuplas[max:]
            funciones.append(nombre_funcion)
            num_funcion+=1
        vba_global="\r\n".join ( funciones )
        vba_resultado=vba_parcial+funcion_global.format ( vba_global )
        return "Option Explicit\r\n"+vba_resultado
        #gf.anadir_a_fichero(nombre_modulo,vba_resultado)