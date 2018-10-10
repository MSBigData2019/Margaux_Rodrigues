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

    
# A. Ventes du dernier quarter
def get_quarter_results(soup):
    """
    Read and return the quarter results estimate (mean) for December 2018 in string format
    """
    financials_table = soup.findAll("td", {"class": "dataTitle"})
    for i in range(len(financials_table)):
        if 'SALES' in financials_table[i].text.strip():
            items_financials = financials_table[i].findAllNext("td")
            for i in range(len(items_financials)):
                if ('Quarter' in items_financials[i].text) &  ('Dec-18' in items_financials[i].text):
                    quarterResult = items_financials[i].findAllNext("td", {"class" : "data"})
                    return quarterResult[1].text.strip()

# B. Prix de l'action et sa dernière variation
def get_share_price(soup):
    """
    Read and return share price of the stock
    """
    quote_details = soup.find("span", {"class" : "nasdaqChangeHeader"})
    share_price  = quote_details.findNext("span")
    return share_price.text.strip()

def get_share_percentage_var(soup):
    """
    Read and return the percentage change of share price
    """
    quote_details = soup.find("div", {"class" : "sectionQuote priceChange"})
    price_change = quote_details.find("span", {"class" : "valueContentPercent"})
    return price_change.text.strip()

# C. Pourcentage de parts détenues par des institutionnels
def get_instit_part(soup):
    """
    Read and return percentage of institutional ownership
    """
    small_table = soup.findAll("div", {'class':'moduleHeader'})
    # Look for insitutional table
    for i in range(len(small_table)):
        if 'Institutional' in small_table[i].h3.text.strip():
           ownership_instit  = small_table[i].findNext('td', {'class':'data'})
    return ownership_instit.text.strip()

# D. Didivend yield de la société, du secteur et de l'industrie
def get_dividends(soup):
    """
    Read and return the dividend yield as a table [company, sector, industry]
    """
    small_table = soup.findAll("div", {'class':'moduleHeader'})
    dividend_table    = small_table[3].findAllNext('td', {'class':'data'})
    company_dividend  = dividend_table[0].text.strip()
    sector_dividend   = dividend_table[1].text.strip()
    industry_dividend = dividend_table[2].text.strip()
    return [company_dividend, sector_dividend, industry_dividend]
    
# 0. Read pages

companies = ['LVMH.PA', 'AIR.PA', 'DANO.PA']
for i in range(len(companies)):
    url = "https://www.reuters.com/finance/stocks/financial-highlights/" + companies[i]
    print(companies[i])
    page = urlopen(url).read()
    soup = BeautifulSoup(page, 'lxml')
    print('Quarter Dec 1 result : \n' + get_quarter_results(soup))
    print('Share price : \n' + get_share_price(soup))
    print('Price change percentage :\n' + get_share_percentage_var(soup))
    print('Pourcentage de détention institutionnel :\n' + get_instit_part(soup))
    print('Dividende de la société : \n' + get_dividends(soup)[0] + \
          '\nDividende du secteur : \n' + get_dividends(soup)[1] + \
          '\nDividende de l\'industrie : \n' + get_dividends(soup)[2] )
