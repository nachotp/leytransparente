from pymongo import *
# import json
from math import pow


def score(porc, cont):
    scr = 0
    if cont == "SI":
        scr = 10000
    if porc <= 50:
        scr += pow(2, (porc / 17.48))
    else:
        scr += pow(5, (porc / 17.48))
    return scr


def conflicto_patrimonio(kwrds):
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["declaraciones"]


    query = mycol.find(
        {"Meta": True, "Derechos_Acciones_Chile": {"$elemMatch": {"Giro_Registrado_SII": {"$in": kwrds}}}},
        {"_id": 1, "Id_Declaracion": 1, "Datos_del_Declarante": 1,
         "Derechos_Acciones_Chile": {"$elemMatch": {"Giro_Registrado_SII": {"$in": kwrds}}}}
    )
    print(query is not None)
    matches = []
    for person in query:
        name = ""
        for nombre in person["Datos_del_Declarante"]["nombre"].split():
            name += nombre.lower().capitalize() + " "
        nombre =  name + person["Datos_del_Declarante"]["Apellido_Paterno"].lower().capitalize() + " " + person["Datos_del_Declarante"]["Apellido_Materno"].lower().capitalize()
        idec = person["_id"]

        # TODO: Le estamos agregando distintos scores para una misma persona ?
        for emp in person["Derechos_Acciones_Chile"]:
            porc = float(emp["Cantidad_Porcentaje"])
            cont = emp["Tiene_Calidad_Controlador"]
            # razon = emp["Nombre_Razon_Social"]
            scr = score(porc, cont)
            matches.append((scr, nombre, idec, emp))
    matches.sort(reverse=True)


    return matches
