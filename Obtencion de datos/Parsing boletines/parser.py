import pandas as pd
import json
import io

dfboletines = pd.read_csv("tagsBoletines.csv", sep=";")
dfcomision = pd.read_csv("VotosComision.csv", sep=";")
dfsala = pd.read_csv("VotosSala.csv", sep=";")


boletines = dfboletines['Boletin'].unique().tolist()
materias  = dfboletines['Materia'].unique().tolist()
print(len(materias))
diputados = dfsala.DIPUTADO.unique().tolist()

dictputados = {}

for dip in diputados:
    dictputados[dip] = {}

dict_boletines = dfboletines.groupby('Boletin')['Materia'].apply(list).to_dict()

for dip,votos in dfsala.groupby('DIPUTADO')['BOLETIN', 'VOTACION']:
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