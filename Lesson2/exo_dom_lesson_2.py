#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 17:27:07 2018
@author: margaux
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen

# EXERCICE : CRAWLER LE SITE DE REUTERS : AIBRBUS, LVMH et DANONE
# Analyser les performances financières des sociétés cotées pour décider d'une stratégie d'investissement.
# Je vous demande donc de récupérer les infos suivantes :
# les ventes au quartier à fin décembre 2018
# le prix de l'action et son % de changement au moment du crawling
# le % Shares Owned des investisseurs institutionels
# le dividend yield de la company, le secteur et de l'industrie

# 0. Read page
url = "https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA"
page = urlopen(url).read()
soup = BeautifulSoup(page, 'lxml')

# A. Ventes du dernier quarter
financials_table = soup.find("table", {"class": "dataTable"})
quarter_line  = 0
col_mean      = 2
resultsLine   = financials_table.findAll("tr", {"class" : "stripe"})
quarterResult = resultsLine[quarter_line].findAll("td", {"class" : "data"})
# Résultat final !
print('Quarter Dec 1 result : \n' + quarterResult[2].text.strip())

# B. Prix de l'action et sa dernière variation
quote_details = soup.findAll("div", {"class" : "sectionQuoteDetail"})
share_price  = quote_details[0].findAll("span")[1]
print('Share price : \n' + share_price.text.strip())
price_change = quote_details[1].find("span", {"class" : "valueContentPercent"})
print('Price change percentage :\n' + price_change.text.strip())

# C. Pourcentage de parts détenues par des institutionnels
small_table = soup.findAll("div", {'class':'moduleHeader'})
ownership_instit = small_table[12].findNext('td', {'class':'data'})
print(ownership_instit.text)

# D. Didivend yield de la société, du secteur et de l'industrie
dividend_table    = small_table[3].findAllNext('td', {'class':'data'})
company_dividend  = dividend_table[0]
sector_dividend   = dividend_table[1]
industry_dividend = dividend_table[2]
print('Dividende de la société : \n' + company_dividend.text + \
      '\nDividende du secteur : \n' + sector_dividend.text + \
      '\nDividende de l\'industrie : \n' + industry_dividend.text)