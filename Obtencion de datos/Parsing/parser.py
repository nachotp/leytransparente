import pandas as pd
import json
import io
import re
from unicodedata import normalize
from Parsing_Declaraciones.dec_parser import parser_dec

declaraciones = parser_dec("Parsing_Declaraciones/declaraciones.json")
arch = open("Parsing boletines/votos.json","r", encoding='utf8')
json_votos = arch.read()
parsed = json.loads(json_votos)
for name in parsed:
    name = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", name), 0, re.I)
    name = normalize( 'NFC', name)
    name = name.upper().split()
    name = name[0] + " " + name[1]
    try:
        print(declaraciones[name])
    except KeyError as e:
        pass