#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:34:13 2018

@author: margaux
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from queue import Queue
from threading import Thread

url = 'https://www.insee.fr/fr/statistiques/1280737'
get_page = requests.get(url)
insee_page = BeautifulSoup(get_page.text, 'lxml')
liste_communes = insee_page.find('table', {'id' : 'produit-tableau-tableau2'}).findChildren('td', {'class' : 'texte'})
plus_grandes_communes = []
for commune in liste_communes:
    plus_grandes_communes.append(commune.text.strip())
print(plus_grandes_communes)

# Distances
