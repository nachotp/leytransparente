import pandas as pd
import json
import io
import re
from unicodedata import normalize   

def parser_dec(archivo):
    with open(archivo, 'r', encoding="utf8") as arch:
        declaraciones = json.load(arch)

    dic = {}
    for declaracion in declaraciones:
        try:
            name = declaracion["Datos_del_Declarante"]["Apellido_Paterno"] + " " + declaracion["Datos_del_Declarante"]["Apellido_Materno"]
            name = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", name), 0, re.I)
            name = normalize( 'NFC', name)
            raw_id = str(declaracion[(list(declaracion.keys())[1])])
            id_declaracion = re.search(r" '(.*)'}", raw_id, re.M|re.I).group(1)
            dic[name] = (id_declaracion,[])
            acciones = declaracion['Derechos_Acciones_Chile']
            for accion in acciones:
                dic[name][1].append(accion['Giro_Registrado_SII'])
        except KeyError:
            pass
    return dic