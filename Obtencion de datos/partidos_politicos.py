import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import pymongo

def partidos():
    url = "https://www.camara.cl/camara/diputados.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    """url = "https://www.camara.cl/camara/diputados.aspx"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        tabla_diputados = soup.findAll("li",{"class" : "alturaDiputado"})
        
        #con esto se obtiene la url de donde se pretende sacar los apellidos para buscar en la BD
        a=tabla_diputados[0].find("h5").find("a")["href"] #'diputado_detalle.aspx?prmid=1008'
        
        #con esto se obtiene el partido politico al cual pertenecen
        b=tabla_diputados[0].findAll("li")[-1].find("a").get_text()
        b.strip().split("\n")[1].strip()
        """