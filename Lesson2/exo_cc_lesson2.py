# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

# Dell ou Acer les plus soldés sur rue du commerce / Darty ?
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

url_dell = "https://www.darty.com/nav/achat/informatique/ordinateur_portable/marque__dell__DELL.html"
req = Request(url_dell, headers={'User-Agent': 'Mozilla/5.0'})
html_dell = urlopen(req).read()
soup = BeautifulSoup(html_dell, 'lxml')
reduc_a = soup.findAll("p", {"class": "darty_prix_barre_remise darty_small separator_top"})

url_acer = 'https://www.darty.com/nav/achat/informatique/ordinateur_portable/marque__acer__ACER.html'
req_acer = Request(url_dell, headers={'User-Agent': 'Mozilla/5.0'})
html_acer = urlopen(req_acer).read()
soup_dell = BeautifulSoup(html_acer, 'lxml')
reduc_d = soup_dell.findAll("p", {"class": "darty_prix_barre_remise darty_small separator_top"})

sum_reduc_a = len(reduc_a)
sum_reduc_d = len(reduc_d)

dell_reduc = []
for i in range(len(reduc_d)):
    dell_reduc = dell_reduc.append(reduc_d[i]).text