import pandas as pd
import json
import io

declaraciones = open("declaraciones.txt",'r')
data = json.load(declaraciones)