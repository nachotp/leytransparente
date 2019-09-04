import requests
import urllib.request
import re

from bs4 import BeautifulSoup

import json

import pymongo

def update_meta():
    myclient = pymongo.MongoClient(
        "mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
        "=true&w=majority")
    mydb = myclient["leytransparente"]

    mycol = mydb["prueba_chris"]

    mycol.update_many({"Meta":True}, {"$set": {"meta.actual": True , "partido":None}})
    mycol.update_many({"Meta": False}, {"$set": {"meta.actual": False , "partido":None}})
    mycol.update_many({}, {"$unset": {"Meta": 'null'}})

def partido():
    myclient = pymongo.MongoClient(
        "mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
        "=true&w=majority")
    mydb = myclient["leytransparente"]

    mycol = mydb["prueba_chris"]

    url = "https://www.camara.cl/camara/diputados.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tabla_diputados = soup.findAll("li", {"class": "alturaDiputado"})

    for diputado in tabla_diputados:
        a = diputado.find("h5").find("a")  # tag donde esta el nombre
        name = a.text.strip().split("\n")[1].strip().upper()  # "NOMBRE APELLIDO"

        b = diputado.findAll("li")[-1].find("a").get_text()  # tag donde esta el partido
        partido = b.strip().split("\n")[1].strip()  # sigal del partido PS por ejemplo

        lista_ids = buscar(name.split(" ")[0], name.split(" ")[1])
        if len(lista_ids) > 0:
            for id in lista_ids:
                mycol.update_one({"_id": id}, {"$set": {"partido": partido}})

    #a = tabla_diputados[0].find("h5").find("a") #tag donde esta el nombre
    #name = a.text.strip().split("\n")[1].strip().upper() #"NOMBRE APELLIDO"

    #b = tabla_diputados[0].findAll("li")[-1].find("a").get_text() #tag donde esta el partido
    #partido = b.strip().split("\n")[1].strip() #sigal del partido PS por ejemplo

    #print(partido)
    #print(name.split(" ")[0])
    #print(name.split(" ")[1])

    #lista_ids = buscar(name.split(" ")[0],name.split(" ")[1])
    #if len(lista_ids) > 0:
        #for id in lista_ids:
            #mycol.update_one({"_id": id }, {"$set": {"meta.partido": partido}})

def buscar(nombre,apellido):
    myclient = pymongo.MongoClient(
        "mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
        "=true&w=majority")
    mydb = myclient["leytransparente"]

    mycol = mydb["prueba_chris"]
    ids = []
    encontrado = mycol.find({'Datos_del_Declarante.Apellido_Paterno': {'$regex': apellido}, "Datos_del_Declarante.nombre":{'$regex': nombre}})
    for document in encontrado:
        #print(document["_id"])
        ids.append(document["_id"])
    print(ids)
    return ids



def cargar_info():
    myclient = pymongo.MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                "=true&w=majority")
    mydb = myclient["leytransparente"]

    mycol = mydb["prueba_chris"]

    #diputados = open("E:\Proyects\leytransparente\Obtencion de datos\Tagging de leyes\JsonInfoProbidad.json", encoding="utf-8") En Windows
    diputados = open("/Users/christophergilbertcarroza/Git Projects/leytransparente/Obtencion de datos/Tagging de leyes/JsonInfoProbidad.json", encoding = "utf-8") #En Mac
    data = json.load(diputados)
    largos =[]
    #f = open("declaraciones.txt", "w")
    daata = {}
    daata["declaraciones"]=[]
    for diputado in data:
        #url_declaracion = diputado["Declaracion"]["value"]
        status = 0
        while (status != 200):
            url_declaracion = diputado["Declaracion"]["value"]
            response = requests.get(url_declaracion)
            status = response.status_code

        response = requests.get(url_declaracion)
        soup = BeautifulSoup(response.text, "html.parser")
        declaracion = soup.findAll("span",{"property" : "dip:jsonCargado"})[0].text
        #print(type(declaracion))
        declaracion = json.loads(declaracion)
        #print(type(declaracion))
        x = mycol.insert_one(declaracion)
    mycol.update_many({}, {"$set": {"Meta.actual": True}})
        #f.write(declaracion)
        #daata["declaraciones"].append(declaracion)
        #print(declaracion)
        #largos.append(len(declaracion))
    #json.dump(daata,f, indent=4)
    #f.close()
    #print(largos)
    #print(len(largos))

def actual():
    myclient = pymongo.MongoClient(
        "mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
        "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["prueba_chris"]

    newvalue = {"$set":{"Meta": bool(False)}}

    for x in mycol.find():
        print(x)
        if(x["Meta"] == bool(True)):
            print("ja")
            for y in mycol.find():
                print(y)
                if(x["_id"] != y["_id"]):
                    if(x["Datos_del_Declarante"]["nombre"] == y["Datos_del_Declarante"]["nombre"] and x['Datos_del_Declarante']['Apellido_Paterno'] == y['Datos_del_Declarante']['Apellido_Paterno'] and x['Datos_del_Declarante']['Apellido_Materno'] == y['Datos_del_Declarante']['Apellido_Materno']):
                        if(x["Fecha_de_la_Declaracion"]>y["Fecha_de_la_Declaracion"]):
                            query = {"_id" : y["_id"]}
                            mycol.update_one(query,newvalue)
                        else:
                            query = {"_id": x["_id"]}
                            mycol.update_one(query, newvalue)


def cargar_actualizaciones():
    myclient = pymongo.MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]

    mycol = mydb["prueba_chris"]

    #diputados = open("E:\Proyects\leytransparente\Obtencion de datos\Tagging de leyes\JsonInfoProbidadAct.json",
     #                encoding="utf-8")
    diputados = open(
        "/Users/christophergilbertcarroza/Git Projects/leytransparente/Obtencion de datos/Tagging de leyes/JsonInfoProbidadAct.json",
        encoding="utf-8")  # En Mac
    data = json.load(diputados)
    daata = {}
    daata["declaraciones"] = []
    for diputado in data:
        url_declaracion = diputado["Declaracion"]["value"]
        response = requests.get(url_declaracion)
        soup = BeautifulSoup(response.text, "html.parser")
        declaracion = soup.findAll("span", {"property": "dip:jsonCargado"})[0].text
        #print(declaracion)
        declaracion = json.loads(declaracion)

        for x in mycol.find({"Meta":True , "Datos_del_Declarante.nombre":declaracion["Datos_del_Declarante"]["nombre"],"Datos_del_Declarante.Apellido_Paterno": declaracion["Datos_del_Declarante"]["Apellido_Paterno"], "Datos_del_Declarante.Apellido_Materno": declaracion["Datos_del_Declarante"]["Apellido_Materno"]}) :
            if(x["Id_Declaracion"] != declaracion["Id_Declaracion"]):
                if(x["Fecha_de_la_Declaracion"] > declaracion["Fecha_de_la_Declaracion"]):
                    declaracion["Meta"]=False
                else:
                    declaracion["Meta"]=True
                    query = {"_id": x["_id"]}
                    newvalue = {"$set": {"Meta": bool(False)}}
                    mycol.update_one(query, newvalue)
                    mycol.insert_one(declaracion)

        #print(type(declaracion))
        #x = mycol.insert_one(declaracion)

#cargar_info()
#actual()
#cargar_actualizaciones()
update_meta()
partido()
#buscar('RICARDO','CELIS')