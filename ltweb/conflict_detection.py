from math import pow
from .conn import DBconnection
from gensim.models import KeyedVectors
import numpy as np
from numpy.linalg import norm
from nltk.tag import StanfordPOSTagger
import os


class EmbeddingPredictor:

    def __init__(self, filename='fasttext-esp.bin', lim=500000):
        self.we = KeyedVectors.load_word2vec_format(filename, binary=True, limit=lim)

    def to_vector(self, texto):
        tokens = texto.split()
        vec = np.zeros(300)
        act = ""
        for word in tokens:
            # si la palabra está la acumulamos
            if word in self.we:
                act += word + " "
                vec += self.we[word]

        print(f"Vectorized: {act}")
        return vec / norm(vec)

    def similarity(self, texto_1, texto_2):
        vec_1 = self.to_vector(texto_1)
        vec_2 = self.to_vector(texto_2)
        sim = vec_1 @ vec_2
        return sim

def extract_nouns(self, text, route):
    java_path = route
    os.environ['JAVAHOME'] = java_path
    para = text.lower()
    stanford_dir = ".\\stanford-postagger-full-2018-10-16"
    modelfile = stanford_dir+"\\models\\spanish.tagger"
    jarfile=stanford_dir+"\\stanford-postagger.jar"
    tagger=StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)
    tags = tagger.tag(para.split())
    nouns = []
    for tag in tags:
        if tag[1][0] == "n" and tag[0] not in nouns:
            nouns.append(tag[0])
    nouns = ' '.join(list(set(nouns)))
    return nouns

def score(porc, cont):
    scr = 0
    if cont == "SI":
        scr = 10000
    if porc <= 50:
        scr += pow(2, (porc / 17.48))
    else:
        scr += pow(5, (porc / 17.48))
    return scr


def conflicto_embedding(tags):
    myclient = DBconnection()
    mycol = myclient.get_collection("declaraciones")

    wp = EmbeddingPredictor()
    print("Embeddings Cargados")

    query = mycol.find(
        {"Meta": True},
        {"_id": 1, "Id_Declaracion": 1, "Datos_del_Declarante": 1, "Derechos_Acciones_Chile": 1}
    )

    print("Declaraciones cargadas")

    matches = []
    for person in query:
        name = ""
        for nombre in person["Datos_del_Declarante"]["nombre"].split():
            name += nombre.lower().capitalize() + " "
        nombre = name + person["Datos_del_Declarante"]["Apellido_Paterno"].lower().capitalize() + " " + \
                 person["Datos_del_Declarante"]["Apellido_Materno"].lower().capitalize()
        idec = person["_id"]

        for emp in person["Derechos_Acciones_Chile"]:
            porc = float(emp["Cantidad_Porcentaje"])
            cont = emp["Tiene_Calidad_Controlador"]
            # razon = emp["Nombre_Razon_Social"]
            scr = score(porc, cont)
            matches.append((scr, nombre, idec, emp))


def conflicto_patrimonio(kwrds):
    myclient = DBconnection()
    mycol = myclient.get_collection("declaraciones")

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
        nombre = name + person["Datos_del_Declarante"]["Apellido_Paterno"].lower().capitalize() + " " + person["Datos_del_Declarante"]["Apellido_Materno"].lower().capitalize()
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
