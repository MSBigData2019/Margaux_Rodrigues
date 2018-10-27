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
import re

def soup_request(url):
    req = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
    if req.status_code != 200:
        print('Echec de la requête')
        exit
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup

# get price
def get_car_price_from_soup(soup):
    a = soup.find('div', {'class':'gpfzj'})
    price = str(a.find_next('strong').text)
    price_regex = re.compile(r"\d+\s+\d+")
    price_find = re.search(price_regex, price).group(0)
    price_find = re.sub(r"\s+", "", price_find)
    return int(price_find)

# Autres infos
def get_year_from_soup(soup):
    infos_generales = soup_annonce.find('ul', {'class' : 'infoGeneraleTxt column2'})
    return int(infos_generales.findNext('span').text)

def get_mileage_from_soup(soup):
    infos_generales = soup_annonce.find('ul', {'class' : 'infoGeneraleTxt column2'})
    kilometrage = infos_generales.findNext('span').findNext('span').text
    kilometrage = re.sub(r"\s+|[a-z]", "", kilometrage)
    return int(kilometrage)

def add_ad_to_data(soup, ad_number, data):
    data['ad_number'].append(ad_number)
    data['price, km, year'].append([get_car_price_from_soup(soup), get_mileage_from_soup(soup), get_year_from_soup(soup)])
# -------------------------------------------
    
brand  = 'RENAULT'
model  = 'ZOE'
region = 'IDF%2CFR-PAC%2CFR-NAQ'
url = 'https://www.lacentrale.fr/listing?makesModelsCommercialNames=' + brand + '%3A' + model + '&regions=FR-' + region
html = requests.get(url)
soup = BeautifulSoup(html.content, features="lxml")
# Get number of responses for request
number_of_cars = int(soup.find('span', {'class':'numAnn'}).text)

# Create dataset
cars_renault_zoe = {'ad_number' : [],
                    'price, km, year' : []
                    }
links=[]
link_list = soup.findAll('a', class_='linkAd ann')
for link in link_list:
    links.append(link['href'])

# ouvrir une annonce :
prefix = 'https://www.lacentrale.fr'
for i in range(len(links)):
    url_annonce = prefix + links[i]
    soup_annonce = soup_request(url_annonce)
    add_ad_to_data(soup_annonce, links[i], cars_renault_zoe)

# create dataframe with results
df = pd.DataFrame(cars_renault_zoe)
df2 = pd.DataFrame(df['price, km, year'].values.tolist(), columns=['Price', 'Km', 'Year'])