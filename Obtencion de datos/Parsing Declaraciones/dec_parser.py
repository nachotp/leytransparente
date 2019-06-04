import pandas as pd
import json
import io
import re

with open('declaraciones.json', 'r', encoding="utf8") as arch:
    declaraciones = json.load(arch)

dic = {}
for declaracion in declaraciones:
    try:
        raw_id = str(declaracion[(list(declaracion.keys())[1])])
        id_declaracion = re.search(r" '(.*)'}", raw_id, re.M|re.I).group(1)
        dic[id_declaracion] = []
        acciones = declaracion['Derechos_Acciones_Chile']
        for accion in acciones:
           dic[id_declaracion].append(accion['Giro_Registrado_SII'])
    except KeyError:
        pass
#
print(dic)