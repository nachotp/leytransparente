import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import pymongo

def get_datos(id_norma_start, id_norma_end):
    #comp = open(file, "r", encoding='latin')
    #compilado = csv.reader(comp, delimiter=";")

    #itercomp = iter(compilado)
    #next(itercomp)

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["leytransparente"]
    mycol = mydb["leyes"]

    f=open("id_normas.txt","w")

    for row in range(id_norma_start, id_norma_end+1):
        ley = {}
        print(row)
        url = "https://www.leychile.cl/Consulta/obtxml?opt=4546&idNorma=" + str(row)
        response = requests.get(url)


        if(response.status_code == 200):
            soup = BeautifulSoup(response.text, "html.parser")

            if(len(soup.findAll("tipo"))>0):
                tipo = soup.findAll("tipo")[0].text
            elif(len(soup.findAll("Tipo"))>0):
                tipo = soup.findAll("Tipo")[0].text
            else:
                tipo=""

            if (tipo == "Ley"):  # condicion para filtrar decreto, codigo, ley, etc
                f.write(str(row)+"\n")
                numero = soup.findAll("numero")[0].text  # obtener el numero de la ley
                nombre = soup.findAll("titulonorma")[0].text

                lista_tags = []

                for tag in soup.findAll("terminolibre"):
                    lista_tags.append(tag.text.strip())  # almacenar los tags en una lista

                url_ley = soup.findAll("url")[0].text  # guardar la url de la ley para mostrarla en caso que sea necesario

                if(len(soup.findAll("Resumen"))>0):
                    resumen = soup.findAll("Resumen")[0].text
                else:
                    resumen = ""

                ley["numero"] = numero
                ley["nombre"] = nombre
                ley["resumen"] = resumen
                ley["tags"] = lista_tags
                ley["url"] = url_ley

                try:
                    x = mycol.insert_one(ley)
                    print("ley insertada correctamente")
                except:
                    print("problemas agregando la ley a la base")
    f.close()



get_datos(21876,1132091)