import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import pymongo

def get_datos():
    #comp = open(file, "r", encoding='latin')
    #compilado = csv.reader(comp, delimiter=";")

    #itercomp = iter(compilado)
    #next(itercomp)

    myclient = pymongo.MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["leyes"]

    #f=open("id_normas.txt","w")

    for leyes in get_ley():
        ley = {}
        status=0
        while(status != 200):
            url = "https://www.leychile.cl/Consulta/obtxml?opt=4546&idLey=" + str(leyes)
            response = requests.get(url)
            status = response.status_code

        soup = BeautifulSoup(response.text, "html.parser")

        if(len(soup.findAll("tipo"))>0):
            tipo = soup.findAll("tipo")[0].text
        elif(len(soup.findAll("Tipo"))>0):
            tipo = soup.findAll("Tipo")[0].text
        else:
            tipo=""

        if (tipo == "Ley" or tipo == "LEY"):  # condicion para filtrar decreto, codigo, ley, etc
            #f.write(str(row)+"\n")
            numero = soup.findAll("numero")[0].text  # obtener el numero de la ley
            nombre = soup.findAll("titulonorma")[0].text

            lista_tags = []

            materias=""
            if(len(soup.findAll("materia"))>0):
                materias="materia"
            elif(len(soup.findAll("materias"))):
                materias = "materias"
            elif(len(soup.findAll("Materia"))):
                materias = "Materias"
            elif(len(soup.findAll("Materias"))):
                materias = "Materias"
            for tag in soup.findAll(materias):
                lista_tags.append(tag.text.strip())  # almacenar los tags en una lista


            url_ley = soup.findAll("url")[0].text  # guardar la url de la ley para mostrarla en caso que sea necesario

            if(len(soup.findAll("resumen"))>0):
                resumen = soup.findAll("resumen")[0].text
            elif(len(soup.findAll("Resumen"))>0):
                resumen = soup.findAll("Resumen")[0].text
            else:
                resumen = "Resumen no disponible"

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
        else:
            print(leyes)
            print("not a ley?")
    #f.close()

def get_ley():
    leyes=[]
    for i in range(1,10):
        url = "https://www.leychile.cl/Consulta/listaresultadosimple?cadena=&npagina="+str(i)+"&itemsporpagina=30&exacta=0&orden=0&tipoviene=0&totalitems=242&seleccionado=0&fc_tn=%2CLey&fc_ra=&fc_rp=&fc_de=&fc_pr=&fc_pb=2016+TO+2018"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for ley in soup.findAll("a",{"class" : "link_norma_tpn"}):
            leyes.append(ley.text.split(" ")[1])

    print(leyes)
    print(len(leyes))
    return leyes
#get_ley()


get_datos()