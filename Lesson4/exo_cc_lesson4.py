# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd
import json
import re

# extraire equivalent traitement pour chacun des produits
a = requests.get('https://open-medicaments.fr/api/v1/medicaments?query=parac%C3%A9tamol')
results = pd.read_json(a.content)
results['Dosage'] = results.denomination.apply(lambda x: x.split(' ')[2])
results['Unite'] = results.denomination.apply(lambda x: x.split(' ')[3][0:-1])

# VERSION REGEX (CORR)
reg = r',(.*)'
serie = results['denomination']
serie.str.extract(reg)

autre = requests.get('https://open-medicaments.fr/api/v1/medicaments/65701216')
autre_json = json.loads(autre.content)
print(autre_json.presentations)
pass
#results['Dosage'] = results['codeCIS'].apply (
#        lambda x: get_dosage(x))
#print(results)

