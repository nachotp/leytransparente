from math import pow
from .conn import DBconnection
from gensim.models import KeyedVectors
import numpy as np
from numpy.linalg import norm
from django.conf import settings
from nltk.tag import StanfordPOSTagger
import string
import os
import operator

class EmbeddingPredictor:

    def __init__(self, filename='fasttext-esp.bin', lim=500000):
        if "JAVAHOME" not in os.environ:
            assert ("JAVA_HOME" in os.environ), "JAVA must be installed and accesible from path."
            os.environ['JAVAHOME'] = str(os.environ['JAVA_HOME'])

        tools_dir = settings.TOOLS_DIR

        self.we = KeyedVectors.load_word2vec_format(os.path.join(tools_dir, filename), binary=True, limit=lim)

        modelfile = os.path.join(tools_dir, "spanish.tagger")
        jarfile = os.path.join(tools_dir, "stanford-postagger.jar")

        self.tagger = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)

    def to_vector(self, texto: str):
        tokens = texto.split()
        vec = np.zeros(300)
        act = ""
        for word in tokens:
            # si la palabra está la acumulamos
            if word in self.we:
                act += word + " "
                vec += self.we[word]

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
    print("BD Conectada")

    wp = EmbeddingPredictor()
    print("Embeddings Cargados")

    query = mycol.find(
        {"Meta": True, "Derechos_Acciones_Chile": {"$exists": True}},
        {"_id": 1, "Id_Declaracion": 1, "Datos_del_Declarante": 1, "Derechos_Acciones_Chile": 1}
    )

    print("Declaraciones cargadas")

    tags = ' '.join(tags)
    sust = wp.extract_nouns(tags)
    vector_ley = wp.to_vector(sust)

    print("Ley vectorizada")

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
            giro = emp["Giro_Registrado_SII"] if "Giro_Registrado_SII" in emp else ""
            razon = emp["Nombre_Razon_Social"]

            giro = giro.lower().translate(str.maketrans('', '', string.punctuation))
            razon = razon.lower().translate(str.maketrans('', '', string.punctuation))

            # giro_vec = wp.to_vector(wp.extract_nouns(giro.lower()))
            giro_vec = wp.to_vector(giro)
            cos_sim = wp.similarity(giro_vec, vector_ley)

            if cos_sim > 0.55:
                scr = score(porc, cont)
                matches.append((cos_sim, scr, nombre, idec, emp))

    matches.sort(key=operator.itemgetter(0, 1), reverse=True)

    return matches


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
        nombre = name + person["Datos_del_Declarante"]["Apellido_Paterno"].lower().capitalize() + " " + \
                 person["Datos_del_Declarante"]["Apellido_Materno"].lower().capitalize()
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
