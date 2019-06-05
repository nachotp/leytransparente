from pymongo import *
import json

myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
mydb = myclient["leytransparente"]
mycol = mydb["declaraciones"]

kwrds = ["AGRICOLA"] 

query = mycol.find(
    {"Derechos_Acciones_Chile": { "$elemMatch" : { "Giro_Registrado_SII": {"$in": kwrds} } } },
    {"Id_Declaracion":1, "Datos_del_Declarante": 1, "Derechos_Acciones_Chile": { "$elemMatch" : { "Giro_Registrado_SII": {"$in": kwrds} } }}
)

for weon in query:
    print(weon["Datos_del_Declarante"]["nombre"])
    for emp in weon["Derechos_Acciones_Chile"]:
        print("\t {Nombre_Razon_Social} - {Cantidad_Porcentaje} % - Controla: {Tiene_Calidad_Controlador}".format(**emp))