import pandas as pd
import json
import io
import re
from unicodedata import normalize   

votos = open("Parsing boletines/votos.json","r")