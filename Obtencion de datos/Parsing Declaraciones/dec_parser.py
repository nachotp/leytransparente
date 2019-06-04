import pandas as pd
import json
import io

with open('declaraciones.json', 'r', encoding="utf8") as arch:
    declaraciones = json.load(arch)

cont = 0
for declaracion in declaraciones:
    try:
        acciones = declaracion['Derechos_Acciones_Chile']
        for accion in acciones:
            print(accion['Giro_Registrado_SII'])
    except KeyError:
        pass