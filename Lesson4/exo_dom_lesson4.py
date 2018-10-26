#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 17:13:57 2018

@author: margaux
"""

"""
L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine. 
Vous utiliserez leboncoin.fr comme source. Si leboncoin ne fonctionne plus vous pouvez vous rabattre sur d'autres sites d'annonces comme lacentrale, paruvendu, autoplus,... Le fichier doit être propre et contenir les infos suivantes : version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd
import json
import re

url = 'https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&regions=FR-IDF%2CFR-PAC%2CFR-NAQ'
req = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
if req != 200:
    print('Echec de la requête')
    exit
soup = BeautifulSoup(req.content)

# Get number of responses for request
number_of_cars = int(soup.find('span', {'class':'numAnn'}).text)


# ouvrir une annonce :
url_annonce = 'https://www.lacentrale.fr/auto-occasion-annonce-69103378129.html'
req_annonce = requests.get(url_annonce, headers = {'User-Agent': 'Mozilla/5.0'})
if req_annonce != 200:
    print(req_annonce)
    print('Echec de la requête')
soup_annonce = BeautifulSoup(req_annonce.content)
a = soup_annonce.find('div', {'class':'gpfzj'})
price = str(a.find_next('strong').text)
price_regex = re.compile(r"\d\s+\d+")
price_find = int(re.search(price_regex, price).group(0))

# Autres infos
infos_generales = soup_annonce.find('ul', {'class' : 'infoGeneraleTxt column2'})
annee = infos_generales.findNext('span')
kilometrage = annee.findNext('span')
