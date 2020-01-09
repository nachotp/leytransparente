from math import pow
from .conn import DBconnection
from gensim.models import KeyedVectors
from numpy.linalg import norm
from django.conf import settings
from nltk.tag import StanfordPOSTagger
import string
import os
import operator
import numpy as np
import pprint


class EmbeddingPredictor:

    def __init__(self, filename='fasttext-esp.bin', lim=600000):
        if "JAVAHOME" not in os.environ:
            assert ("JAVA_HOME" in os.environ), "JAVA must be installed and accesible from path."
            os.environ['JAVAHOME'] = str(os.environ['JAVA_HOME'])

        tools_dir = settings.TOOLS_DIR
        if "java.exe" not in os.environ['JAVAHOME']:
            os.environ['JAVAHOME'] += "\\java.exe"

        self.we = KeyedVectors.load_word2vec_format(os.path.join(tools_dir, filename), binary=True, limit=lim)

        modelfile = os.path.join(tools_dir, "spanish.tagger")
        jarfile = os.path.join(tools_dir, "stanford-postagger.jar")

        self.tagger = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)

    def to_vector(self, texto: str):
        tokens = texto.split()
        vec = np.zeros(300)
        act = ""
        ranks = []
        for word in tokens:
            # si la palabra está la acumulamos
            if word in self.we:
                act += word + " "
                rank = 1 + self.we.wv.vocab[word].index
                vec += self.we[word] * np.sqrt(rank)
                ranks.append(rank)

        return vec / norm(vec) if norm(vec) > 0 else np.zeros(300)

    @staticmethod
    def similarity(vec_1, vec_2):
        sim = vec_1 @ vec_2
        return sim

    def extract_nouns(self, text):
        para = text.lower()
        tags = self.tagger.tag(para.split())
        nouns = []
        for tag in tags:
            if tag[1][0] == "n" and tag[0] not in nouns:
                nouns.append(tag[0])
        nouns = ' '.join(list(set(nouns)))
        return nouns


def score(porc, cont):
    scr = 0
    porc = porc if porc < 100 else 100
    if cont == "SI":
        scr = 10000
    if porc <= 50:
        scr += pow(2, (porc / 17.48))
    else:
        scr += pow(3, (porc / 17.48))
    return scr


def conflicto_embedding(tags):
    myclient = DBconnection()
    mycol = myclient.get_collection("declaraciones")
    mycol2 = myclient.get_collection("indirectos")
    print("BD Conectada")

    wp = EmbeddingPredictor()
    print("Embeddings Cargados")

    query = mycol.find(
        {"meta.actual": True, "Derechos_Acciones_Chile": {"$exists": True}},
        {"_id": 1, "Id_Declaracion": 1, "Datos_del_Declarante": 1, "Derechos_Acciones_Chile": 1}
    )
    query_familiar = mycol2.find(
        {"Derechos_Acciones_Chile": {"$exists": True}},
        {"_id": 1, "Parlamentario": 1, "Parentesco": 1, "Derechos_Acciones_Chile": 1,"Datos_del_Pariente": 1, "tipo": 1}
    )

    query_lobby = mycol2.find(
        {"Representa": {"$exists": True}},
        {"_id": 1, "Parlamentario": 1, "Representa": 1, "Datos_del_Lobista": 1,"tipo": 1}
    )
   #print("lobby")
   #for document in query_familiar:
   #    pprint(document)

    tags = ' '.join(tags)
    sust = wp.extract_nouns(tags)
    vector_ley = wp.to_vector(sust)

    print(f"Ley vectorizada: {sust}")

    matches = []
    prematch = []

    print("Revisando pre-candidatos")
    for person in query:

        for emp in person["Derechos_Acciones_Chile"]:

            giro = emp["Giro_Registrado_SII"] if "Giro_Registrado_SII" in emp else ""

            giro = giro.lower().translate(str.maketrans('', '', string.punctuation))

            # giro_vec = wp.to_vector(wp.extract_nouns(giro.lower()))
            giro_vec = wp.to_vector(giro)
            cos_sim = wp.similarity(giro_vec, vector_ley)

            if cos_sim > 0.55:
                prematch.append(person)

    print("Filtrando candidatos")
    for person in prematch:
        name = ""
        tipo = "directo"
        for nombre in person["Datos_del_Declarante"]["nombre"].split():
            name += nombre.lower().capitalize() + " "
        nombre = name + person["Datos_del_Declarante"]["Apellido_Paterno"].lower().capitalize() + " " + \
            person["Datos_del_Declarante"]["Apellido_Materno"].lower().capitalize()
        idec = person["_id"]

        for emp in person["Derechos_Acciones_Chile"]:

            porc = float(emp["Cantidad_Porcentaje"])
            cont = emp["Tiene_Calidad_Controlador"]
            giro = emp["Giro_Registrado_SII"] if "Giro_Registrado_SII" in emp else ""
            razon = emp["Nombre_Razon_Social"]

            giro = giro.lower().translate(str.maketrans('', '', string.punctuation))
            print(giro)
            # giro = wp.extract_nouns(giro)
            #   razon = razon.lower().translate(str.maketrans('', '', string.punctuation))
            # giro_vec = wp.to_vector(wp.extract_nouns(giro.lower()))
            giro_vec = wp.to_vector(giro)
            cos_sim = wp.similarity(giro_vec, vector_ley)
            print(giro, ">", cos_sim)
            if cos_sim > 0.5:
                scr = score(porc, cont)
                matches.append((cos_sim, scr, nombre, idec, emp,tipo , list(giro_vec)))

    for familiar in query_familiar:
        nombre = ""
        tipo = "indirecto"
        for name in familiar["Parlamentario"].split():
            print("en conflicto indirecto familiar:" + familiar["Parlamentario"])
            nombre += name.lower().capitalize() + " "
        idec = familiar["_id"]
        involucrado = familiar["Datos_del_Pariente"]["nombre"] + " " + familiar["Datos_del_Pariente"]["Apellido_Paterno"] + " " + familiar["Datos_del_Pariente"]["Apellido_Materno"]

        for empresa in familiar["Derechos_Acciones_Chile"]:
            print(list(empresa))
            porc = float(empresa["Cantidad_Porcentaje"])
            giro = empresa["Giro_Registrado_SII"] if "Giro_Registrado_SII" in empresa else ""
            razon = empresa["Nombre_Razon_Social"]

            giro = giro.lower().translate(str.maketrans('', '', string.punctuation))
            razon = razon.lower().translate(str.maketrans('', '', string.punctuation))
            giro_vec = wp.to_vector(giro)
            cos_sim = wp.similarity(giro_vec, vector_ley)
            print(cos_sim)
            if cos_sim > 0.55:
                matches.append((cos_sim, 0, nombre, idec, empresa, tipo, involucrado))

    for lobby in query_lobby:
        nombre = ""
        tipo = "indirecto"
        for name in lobby["Parlamentario"].split():
            nombre += name.lower().capitalize() + " "
        idec = lobby["_id"]
        involucrado = lobby["Datos_del_Lobista"]["nombre"] + " " + lobby["Datos_del_Lobista"]["Apellido_Paterno"] + " " + lobby["Datos_del_Lobista"]["Apellido_Materno"]
        for empresa in lobby["Representa"]:
            print(empresa["Nombre_Razon_Social"])
            razon = empresa["Nombre_Razon_Social"]
            giro = empresa["Giro_Registrado_SII"] if "Giro_Registrado_SII" in empresa else ""
            giro = giro.lower().translate(str.maketrans('', '', string.punctuation))
            razon = razon.lower().translate(str.maketrans('', '', string.punctuation))
            giro_vec = wp.to_vector(giro)
            cos_sim = wp.similarity(giro_vec, vector_ley)

            print(cos_sim)
            if cos_sim > 0.55:
                matches.append((cos_sim, -1, nombre, idec, empresa ,tipo , involucrado))

    matches.sort(key=operator.itemgetter(0, 1), reverse=True)

    return matches
