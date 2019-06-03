import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import json
from os import listdir
from os.path import isfile, join

import itertools
import sys
import time
import threading


class Spinner(object):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self):
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            time.sleep(0.25)
            sys.stdout.write('\b')

comps = [f for f in listdir("compendios") if isfile(join("compendios", f))]

print(comps)

def get_datos(file):
  comp = open(file,"r",encoding='latin')
  compilado = csv.reader(comp, delimiter= ";")
  leyes = {}
  itercomp = iter(compilado)
  next(itercomp)
  for row in itercomp:
    titulo = row[2]
    url = "https://www.leychile.cl/Consulta/obtxml?opt=4546&idNorma="+str(row[5])
    response = requests.get(url)
    try:
      soup = BeautifulSoup(response.text, "html.parser")
      if(soup.findAll("tipo")[0].text == "Ley"): #condicion para filtrar decreto, codigo, ley, etc
        numero = soup.findAll("numero")[0].text #obtener el numero de la ley
        lista_tags=[]
        for tag in soup.findAll("terminolibre"):
          lista_tags.append(tag.text.strip()) #almacenar los tags en una lista
        url_ley = soup.findAll("url")[0].text #guardar la url de la ley para mostrarla en caso que sea necesario
        leyes[int(row[5])] = {
          "title": titulo,
          "numero": numero,
          "tags": lista_tags,
          "url": url_ley
        }
    except Exception as e:

      print("Error:" + str(e))
    
  return leyes

leyes = {}
spinner = Spinner()
spinner.start()

for compendio in comps:
  print(f"Extrayendo tags de {compendio}")
  leyes = {**leyes, **get_datos(join("compendios", compendio))}

spinner.stop()

out = open("tagsleyes.json", "w")

out.write(json.dumps(leyes, indent=2, sort_keys=True))

out.close()