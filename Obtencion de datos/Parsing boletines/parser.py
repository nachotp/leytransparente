import pandas as pd
import json
import io
import re
from unicodedata import normalize   

dfboletines = pd.read_csv("tagsBoletines.csv", sep=";")
dfcomision = pd.read_csv("VotosComision.csv", sep=";")
dfsala = pd.read_csv("VotosSala.csv", sep=";")


boletines = dfboletines['Boletin'].unique().tolist()
materias  = dfboletines['Materia'].unique().tolist()
materias.sort()
with io.open("materias.dat","w", encoding='utf8') as fl:
    fl.write("\n".join(materias))

diputados = dfsala.DIPUTADO.unique().tolist()

dictputados = {}

for dip in diputados:
    dictputados[dip] = {}

dict_boletines = dfboletines.groupby('Boletin')['Materia'].apply(list).to_dict()
for dip,votos in dfsala.groupby('DIPUTADO')['BOLETIN', 'VOTACION']:
    dip = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", dip), 0, re.I)
    dip = dip.upper()
    print(dip)
    for index, row in votos.iterrows():
        try:
            bol_materias = dict_boletines[row["BOLETIN"]]
            if row['VOTACION'] in ["AFIRMATIVO", "A FAVOR"]:
                for mat in bol_materias:
                    if mat not in dictputados[dip]:
                        dictputados[dip][mat] = [0,0]
                    dictputados[dip][mat][0] += 1
            elif row['VOTACION']  == "EN CONTRA":
                for mat in bol_materias:
                    if mat not in dictputados[dip]:
                        dictputados[dip][mat] = [0,0]
                    dictputados[dip][mat][1] += 1
        except KeyError as e:
            pass
            
with io.open("boletines.json","w", encoding='utf8') as fl:
    fl.write(json.dumps(dict_boletines, indent=2, ensure_ascii=False))

with io.open("votos.json","w", encoding='utf8') as fl:
    fl.write(json.dumps(dictputados, indent=2, ensure_ascii=False))