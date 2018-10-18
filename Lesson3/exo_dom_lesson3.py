#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:51:35 2018

@author: margaux
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

def get_main_contrib_crawl(url):
    
    res = requests.get(url)
    html_doc =  res.text
    soup = BeautifulSoup(html_doc, "lxml")
    elt = soup.find("tbody")
    rankings = elt.findAll("th", {'scope' : 'row'})
    
    usernames = [] 
    names = []
    rankings = []
    
    for truc in elt.findAll('tr'):
        user_info = truc.findNext('td').text.split()
        usernames.append(user_info[0])
        if (len(user_info) > 1):
            if len(user_info) > 2:
                username = user_info[1][1:] + ' ' + user_info[2][:-1]
            else:
                username = user_info[1][1:]
        else:
            username = ''
        names.append(username) 
        rankings.append(truc.findNext('th').text[1:])
    
    d = {'Username': usernames, 'Name' : names}
    df = pd.DataFrame(data = d, index = rankings)
    print(df)
        

def main():
    # Crawling
    url = 'https://gist.github.com/paulmillr/2657075'
    # get_main_contrib_crawl(url)
    # using API
    # objectif récupérer pour les top contributeurs le nombre moyen de stars de leurs repos
    # puis les classer 
    url = 'https://api.github.com/users/StephanePEILLET/repos'
    head = {'Authorization': 'token {}'.format('token')}
    get_repo = requests.get(url, headers=head)
    truc = json.loads(get_repo.content)
    print(truc)
    #stragazers_count
if __name__ == '__main__':
    main()
